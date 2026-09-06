"""Smoke-test POST /v1/jobs against a running worker (local or Render)."""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


def _request(method: str, url: str, *, headers: dict[str, str] | None = None, data: bytes | None = None):
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    with urllib.request.urlopen(req, timeout=120) as resp:
        body = resp.read()
        return resp.status, body


def _multipart(fields: dict[str, str], files: dict[str, tuple[str, bytes]]) -> tuple[bytes, str]:
    boundary = "----vibe23workerboundary"
    chunks: list[bytes] = []
    for name, value in fields.items():
        chunks.append(f"--{boundary}\r\n".encode())
        chunks.append(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode())
        chunks.append(value.encode() + b"\r\n")
    for name, (filename, content) in files.items():
        chunks.append(f"--{boundary}\r\n".encode())
        chunks.append(
            f'Content-Disposition: form-data; name="{name}"; filename="{filename}"\r\n'.encode()
        )
        chunks.append(b"Content-Type: application/octet-stream\r\n\r\n")
        chunks.append(content + b"\r\n")
    chunks.append(f"--{boundary}--\r\n".encode())
    return b"".join(chunks), f"multipart/form-data; boundary={boundary}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default=os.getenv("EPLUS_WORKER_URL", "http://127.0.0.1:8000"))
    parser.add_argument("--api-key", default=os.getenv("EPLUS_WORKER_API_KEY") or os.getenv("API_KEY", ""))
    parser.add_argument("--idf", type=Path, required=True)
    parser.add_argument("--epw", type=Path, required=True)
    parser.add_argument("--poll-seconds", type=float, default=5.0)
    parser.add_argument("--timeout-seconds", type=float, default=960.0)
    args = parser.parse_args()
    if not args.api_key:
        print("Set --api-key or EPLUS_WORKER_API_KEY / API_KEY", file=sys.stderr)
        return 2

    base = args.base_url.rstrip("/")
    auth = {"Authorization": f"Bearer {args.api_key}"}
    try:
        _, health_body = _request("GET", f"{base}/healthz")
    except urllib.error.HTTPError as exc:
        print("healthz failed", exc.code, exc.read().decode(), file=sys.stderr)
        return 1
    print("healthz", json.loads(health_body))

    body, content_type = _multipart(
        {"expand_objects": "true"},
        {
            "idf": (args.idf.name, args.idf.read_bytes()),
            "epw": (args.epw.name, args.epw.read_bytes()),
        },
    )
    headers = {**auth, "Content-Type": content_type}
    try:
        status, created_body = _request("POST", f"{base}/v1/jobs", headers=headers, data=body)
    except urllib.error.HTTPError as exc:
        print("create failed", exc.code, exc.read().decode()[:800], file=sys.stderr)
        return 1
    print("create", status, created_body[:500])
    job = json.loads(created_body)
    job_id = job["job_id"]
    deadline = time.time() + args.timeout_seconds
    payload: dict = {}
    while time.time() < deadline:
        _, status_body = _request("GET", f"{base}/v1/jobs/{job_id}", headers=auth)
        payload = json.loads(status_body)
        print("status", payload.get("status"), payload.get("wall_seconds"))
        if payload.get("status") in {"succeeded", "failed"}:
            break
        time.sleep(args.poll_seconds)
    else:
        print("timed out waiting for job", file=sys.stderr)
        return 1
    return 0 if payload.get("status") == "succeeded" else 1


if __name__ == "__main__":
    raise SystemExit(main())
