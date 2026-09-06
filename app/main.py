from __future__ import annotations

import asyncio
import json
import os
import re
import secrets
import shutil
import subprocess
import time
import uuid
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Annotated

from fastapi import (
    BackgroundTasks,
    Depends,
    FastAPI,
    File,
    Form,
    Header,
    HTTPException,
    UploadFile,
)
from fastapi.responses import FileResponse

APP_VERSION = "1.0.0"
JOB_ROOT = Path(os.getenv("JOB_ROOT", "/var/lib/eplus-worker/jobs"))
ENERGYPLUS_EXE = Path(os.getenv("ENERGYPLUS_EXE", "/opt/EnergyPlus-26-1-0/energyplus"))
MAX_UPLOAD_BYTES = int(float(os.getenv("MAX_UPLOAD_MB", "50")) * 1024 * 1024)
SIM_TIMEOUT_SECONDS = int(os.getenv("SIM_TIMEOUT_SECONDS", "900"))
JOB_TTL_SECONDS = int(float(os.getenv("JOB_TTL_HOURS", "24")) * 3600)
MAX_CONCURRENT_JOBS = max(1, int(os.getenv("MAX_CONCURRENT_JOBS", "1")))
_semaphore = asyncio.Semaphore(MAX_CONCURRENT_JOBS)
_idf_version_re = re.compile(r"(?im)^\s*Version\s*,\s*([0-9.]+)\s*;")

@asynccontextmanager
async def lifespan(_: FastAPI):
    JOB_ROOT.mkdir(parents=True, exist_ok=True)
    _cleanup_expired()
    yield


app = FastAPI(
    title="Vibe 23 EnergyPlus Worker",
    version=APP_VERSION,
    description="Runs isolated EnergyPlus 26.1 simulations and returns their output archives.",
    lifespan=lifespan,
)


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _job_dir(job_id: str) -> Path:
    try:
        parsed = uuid.UUID(job_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail="job not found") from exc
    return JOB_ROOT / str(parsed)


def _metadata_path(job_id: str) -> Path:
    return _job_dir(job_id) / "job.json"


def _write_metadata(job_id: str, payload: dict) -> None:
    path = _metadata_path(job_id)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def _read_metadata(job_id: str) -> dict:
    path = _metadata_path(job_id)
    if not path.is_file():
        raise HTTPException(status_code=404, detail="job not found")
    return json.loads(path.read_text(encoding="utf-8"))


def require_api_key(authorization: Annotated[str | None, Header()] = None) -> None:
    expected = os.getenv("API_KEY", "").strip()
    if not expected:
        raise HTTPException(status_code=503, detail="server API_KEY is not configured")
    supplied = ""
    if authorization and authorization.lower().startswith("bearer "):
        supplied = authorization[7:].strip()
    if not supplied or not secrets.compare_digest(supplied, expected):
        raise HTTPException(status_code=401, detail="invalid bearer token")


async def _save_upload(upload: UploadFile, target: Path, expected_suffix: str) -> int:
    if Path(upload.filename or "").suffix.lower() != expected_suffix:
        raise HTTPException(status_code=422, detail=f"expected a {expected_suffix} file")
    size = 0
    with target.open("wb") as handle:
        while chunk := await upload.read(1024 * 1024):
            size += len(chunk)
            if size > MAX_UPLOAD_BYTES:
                target.unlink(missing_ok=True)
                raise HTTPException(status_code=413, detail="upload exceeds configured size limit")
            handle.write(chunk)
    if size == 0:
        target.unlink(missing_ok=True)
        raise HTTPException(status_code=422, detail="uploaded file is empty")
    return size


def _validate_idf(path: Path) -> None:
    text = path.read_text(encoding="utf-8", errors="strict")
    match = _idf_version_re.search(text)
    if not match:
        raise HTTPException(status_code=422, detail="IDF has no Version object")
    version_parts = match.group(1).split(".")
    if version_parts[:2] != ["26", "1"] or any(part != "0" for part in version_parts[2:]):
        raise HTTPException(status_code=422, detail=f"IDF version {match.group(1)} does not match EnergyPlus 26.1")


def _validate_epw(path: Path) -> None:
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        first = handle.readline()
    if not first.upper().startswith("LOCATION,"):
        raise HTTPException(status_code=422, detail="EPW does not begin with a LOCATION header")


def _cleanup_expired() -> None:
    if JOB_TTL_SECONDS <= 0 or not JOB_ROOT.exists():
        return
    cutoff = time.time() - JOB_TTL_SECONDS
    for child in JOB_ROOT.iterdir():
        if child.is_dir() and child.stat().st_mtime < cutoff:
            shutil.rmtree(child, ignore_errors=True)


async def _execute(job_id: str, expand_objects: bool) -> None:
    async with _semaphore:
        root = _job_dir(job_id)
        output = root / "output"
        output.mkdir(exist_ok=True)
        metadata = _read_metadata(job_id)
        metadata.update(status="running", started_at=_now())
        _write_metadata(job_id, metadata)
        cmd = [str(ENERGYPLUS_EXE)]
        if expand_objects:
            cmd.append("-x")
        cmd.extend(["-w", str(root / "weather.epw"), "-d", str(output), "-r", str(root / "input.idf")])
        started = time.perf_counter()
        try:
            process = await asyncio.to_thread(
                subprocess.run,
                cmd,
                capture_output=True,
                text=True,
                timeout=SIM_TIMEOUT_SECONDS,
                check=False,
                cwd=root,
            )
            (output / "console.log").write_text(
                (process.stdout or "") + "\n" + (process.stderr or ""), encoding="utf-8"
            )
            err_text = (output / "eplusout.err").read_text(encoding="utf-8", errors="replace") if (output / "eplusout.err").is_file() else ""
            fatal_count = len(re.findall(r"\*\*\s*Fatal\s*\*\*", err_text, re.IGNORECASE))
            severe_count = len(re.findall(r"\*\*\s*Severe\s*\*\*", err_text, re.IGNORECASE))
            warning_count = len(re.findall(r"\*\*\s*Warning\s*\*\*", err_text, re.IGNORECASE))
            archive = shutil.make_archive(str(root / "results"), "zip", root_dir=root, base_dir="output")
            success = process.returncode == 0 and fatal_count == 0 and severe_count == 0
            metadata.update(
                status="succeeded" if success else "failed",
                completed_at=_now(),
                wall_seconds=round(time.perf_counter() - started, 3),
                return_code=process.returncode,
                fatal_count=fatal_count,
                severe_count=severe_count,
                warning_count=warning_count,
                result_available=Path(archive).is_file(),
            )
        except subprocess.TimeoutExpired:
            metadata.update(
                status="failed",
                completed_at=_now(),
                wall_seconds=round(time.perf_counter() - started, 3),
                error=f"simulation exceeded {SIM_TIMEOUT_SECONDS} seconds",
            )
        except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as exc:
            metadata.update(
                status="failed",
                completed_at=_now(),
                wall_seconds=round(time.perf_counter() - started, 3),
                error=f"worker error: {type(exc).__name__}: {exc}",
            )
        _write_metadata(job_id, metadata)


@app.get("/healthz")
def health() -> dict:
    available = ENERGYPLUS_EXE.is_file() and os.access(ENERGYPLUS_EXE, os.X_OK)
    if not available:
        raise HTTPException(status_code=503, detail="EnergyPlus executable unavailable")
    return {"ok": True, "service_version": APP_VERSION, "energyplus_version": "26.1.0"}


@app.post("/v1/jobs", status_code=202, dependencies=[Depends(require_api_key)])
async def create_job(
    background_tasks: BackgroundTasks,
    idf: Annotated[UploadFile, File(description="EnergyPlus 26.1 IDF")],
    epw: Annotated[UploadFile, File(description="EPW weather file")],
    expand_objects: Annotated[bool, Form()] = True,
) -> dict:
    _cleanup_expired()
    job_id = str(uuid.uuid4())
    root = _job_dir(job_id)
    root.mkdir(parents=True, exist_ok=False)
    try:
        idf_bytes = await _save_upload(idf, root / "input.idf", ".idf")
        epw_bytes = await _save_upload(epw, root / "weather.epw", ".epw")
        _validate_idf(root / "input.idf")
        _validate_epw(root / "weather.epw")
    except Exception:
        shutil.rmtree(root, ignore_errors=True)
        raise
    metadata = {
        "job_id": job_id,
        "status": "queued",
        "created_at": _now(),
        "idf_bytes": idf_bytes,
        "epw_bytes": epw_bytes,
        "expand_objects": expand_objects,
        "result_available": False,
    }
    _write_metadata(job_id, metadata)
    background_tasks.add_task(_execute, job_id, expand_objects)
    return metadata


@app.get("/v1/jobs/{job_id}", dependencies=[Depends(require_api_key)])
def get_job(job_id: str) -> dict:
    return _read_metadata(job_id)


@app.get("/v1/jobs/{job_id}/results", dependencies=[Depends(require_api_key)])
def get_results(job_id: str) -> FileResponse:
    metadata = _read_metadata(job_id)
    archive = _job_dir(job_id) / "results.zip"
    if metadata.get("status") not in {"succeeded", "failed"} or not archive.is_file():
        raise HTTPException(status_code=409, detail="results are not available")
    return FileResponse(archive, media_type="application/zip", filename=f"energyplus-{job_id}.zip")


@app.delete("/v1/jobs/{job_id}", dependencies=[Depends(require_api_key)])
def delete_job(job_id: str) -> dict:
    metadata = _read_metadata(job_id)
    if metadata.get("status") == "running":
        raise HTTPException(status_code=409, detail="a running job cannot be deleted")
    shutil.rmtree(_job_dir(job_id))
    return {"deleted": True, "job_id": job_id}
