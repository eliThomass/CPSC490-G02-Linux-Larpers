from datetime import UTC, datetime

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

import db
from main import app
from models import ScanSession, Scanner


def test_saved_observation_survives_backend_restart(tmp_path, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path / 'restart.db'}")
    db.get_engine.cache_clear()
    with Session(db.get_engine()) as session:
        scanner = Scanner(name="node-1", hardware_model="ESP32", firmware_version="0.1.0")
        scan_session = ScanSession(name="restart", started_at=datetime.now(UTC))
        session.add_all([scanner, scan_session])
        session.commit()
        ids = {"scanner_id": str(scanner.scanner_id), "session_id": str(scan_session.session_id)}

    saved = TestClient(app).post("/observations", json={
        **ids,
        "captured_at": "2026-11-09T12:00:00Z",
        "protocol": "wifi",
    }).json()

    db.get_engine().dispose()
    db.get_engine.cache_clear()

    observations = TestClient(app).get("/observations").json()
    db.get_engine().dispose()
    db.get_engine.cache_clear()
    assert [o["observation_id"] for o in observations] == [saved["observation_id"]]
    assert observations[0]["protocol"] == "wifi"
