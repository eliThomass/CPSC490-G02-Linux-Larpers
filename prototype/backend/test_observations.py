import uuid
from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from db import get_session
from main import app
from models import Base, DetectedDevice, Observation, ScanSession, Scanner

# Tests for the /observations endpoint. 
# These tests check that valid observations are stored in the database, 
# and that invalid observations are rejected and not stored.

@pytest.fixture
def session():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture
def client(session):
    app.dependency_overrides[get_session] = lambda: session
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def ids(session):
    scanner = Scanner(name="node-1", hardware_model="ESP32", firmware_version="0.1.0")
    scan_session = ScanSession(name="test", started_at=datetime.now(UTC))
    session.add_all([scanner, scan_session])
    session.commit()
    return {"scanner_id": str(scanner.scanner_id), "session_id": str(scan_session.session_id)}


def stored(session):
    return session.scalars(select(Observation)).all()


def test_valid_observation_is_stored(client, session, ids):
    response = client.post("/observations", json={
        **ids,
        "captured_at": "2026-11-09T12:00:00Z",
        "protocol": "wifi",
        "observed_address": "aa:bb:cc:dd:ee:ff",
        "address_type": "bssid",
        "rssi_dbm": -60,
        "signal_percent": 80,
        "metadata": {"ssid": "test-network", "channel": 6},
    })
    assert response.status_code == 201
    row = session.get(Observation, uuid.UUID(response.json()["observation_id"]))
    assert row.protocol == "wifi"
    assert row.rssi_dbm == -60
    assert row.signal_percent == 80
    assert row.metadata_ == {"ssid": "test-network", "channel": 6}


def test_observation_without_optional_fields_is_stored(client, session, ids):
    response = client.post("/observations", json={
        **ids,
        "captured_at": "2026-11-09T12:00:00Z",
        "protocol": "bluetooth",
    })
    assert response.status_code == 201
    row = stored(session)[0]
    assert row.device_id is None
    assert row.observed_address is None
    assert row.rssi_dbm is None


def test_observation_with_device_is_stored(client, session, ids):
    device = DetectedDevice(display_name="test device")
    session.add(device)
    session.commit()
    response = client.post("/observations", json={
        **ids,
        "device_id": str(device.device_id),
        "captured_at": "2026-11-09T12:00:00Z",
        "protocol": "bluetooth",
    })
    assert response.status_code == 201
    assert stored(session)[0].device_id == device.device_id


def test_invalid_observation_is_rejected_and_not_stored(client, session, ids):
    response = client.post("/observations", json={**ids, "protocol": "zigbee"})
    assert response.status_code == 422
    fields = {error["loc"][-1] for error in response.json()["detail"]}
    assert fields == {"captured_at", "protocol"}
    assert stored(session) == []


def test_unknown_scanner_is_rejected_and_not_stored(client, session, ids):
    response = client.post("/observations", json={
        **ids,
        "scanner_id": str(uuid.uuid4()),
        "captured_at": "2026-11-09T12:00:00Z",
        "protocol": "wifi",
    })
    assert response.status_code == 422
    assert "Unknown scanner_id" in response.json()["detail"]
    assert stored(session) == []


def test_unknown_device_is_rejected_and_not_stored(client, session, ids):
    response = client.post("/observations", json={
        **ids,
        "device_id": str(uuid.uuid4()),
        "captured_at": "2026-11-09T12:00:00Z",
        "protocol": "wifi",
    })
    assert response.status_code == 422
    assert "Unknown device_id" in response.json()["detail"]
    assert stored(session) == []
