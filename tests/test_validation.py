from __future__ import annotations

import os
from pathlib import Path

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.main import _validate_epw, _validate_idf, app


def test_accepts_energyplus_26_1_idf(tmp_path: Path) -> None:
    path = tmp_path / "model.idf"
    path.write_text("Version, 26.1;\n", encoding="utf-8")
    _validate_idf(path)


def test_rejects_wrong_idf_version(tmp_path: Path) -> None:
    path = tmp_path / "model.idf"
    path.write_text("Version, 25.1;\n", encoding="utf-8")
    with pytest.raises(HTTPException):
        _validate_idf(path)


def test_requires_epw_location_header(tmp_path: Path) -> None:
    path = tmp_path / "weather.epw"
    path.write_text("not-an-epw\n", encoding="utf-8")
    with pytest.raises(HTTPException):
        _validate_epw(path)


def test_healthz_reports_api_key_flag(monkeypatch, tmp_path: Path) -> None:
    fake_exe = tmp_path / "energyplus"
    fake_exe.write_text("x", encoding="utf-8")
    monkeypatch.setattr("app.main.ENERGYPLUS_EXE", fake_exe)
    monkeypatch.setattr(os, "access", lambda *_args, **_kwargs: True)
    monkeypatch.setenv("API_KEY", "")
    client = TestClient(app)
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json()["api_key_configured"] is False
    monkeypatch.setenv("API_KEY", "secret")
    resp2 = client.get("/healthz")
    assert resp2.json()["api_key_configured"] is True


def test_root_endpoint() -> None:
    client = TestClient(app)
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json()["healthz"] == "/healthz"


def test_jobs_require_api_key(monkeypatch) -> None:
    monkeypatch.delenv("API_KEY", raising=False)
    client = TestClient(app)
    resp = client.post("/v1/jobs")
    assert resp.status_code == 503


def test_list_jobs_requires_api_key(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("API_KEY", "secret")
    monkeypatch.setenv("JOB_ROOT", str(tmp_path))
    from app import main as worker_main

    monkeypatch.setattr(worker_main, "JOB_ROOT", tmp_path)
    client = TestClient(worker_main.app)
    resp = client.get("/v1/jobs")
    assert resp.status_code == 401
    resp_ok = client.get("/v1/jobs", headers={"Authorization": "Bearer secret"})
    assert resp_ok.status_code == 200
    body = resp_ok.json()
    assert body["jobs"] == []
    assert body["queue"]["max_concurrent"] >= 1
