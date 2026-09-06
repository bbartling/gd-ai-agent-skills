from pathlib import Path

import pytest
from fastapi import HTTPException

from app.main import _validate_epw, _validate_idf


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

