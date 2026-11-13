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


def add_observation(session, ids, captured_at, device_id=None):
    row = Observation(
        scanner_id=uuid.UUID(ids["scanner_id"]),
        session_id=uuid.UUID(ids["session_id"]),
        device_id=device_id,
        captured_at=captured_at,
        protocol="wifi",
    )
    session.add(row)
    session.commit()
    return row


def test_time_range_returns_only_observations_inside_it(client, session, ids):
    add_observation(session, ids, datetime(2026, 11, 9, 10, tzinfo=UTC))
    inside = add_observation(session, ids, datetime(2026, 11, 9, 12, tzinfo=UTC))
    add_observation(session, ids, datetime(2026, 11, 9, 14, tzinfo=UTC))
    response = client.get("/observations", params={
        "start": "2026-11-09T11:00:00Z",
        "end": "2026-11-09T13:00:00Z",
    })
    assert response.status_code == 200
    assert [o["observation_id"] for o in response.json()] == [str(inside.observation_id)]


def test_device_filter_returns_only_that_devices_observations(client, session, ids):
    device = DetectedDevice(display_name="device a")
    other = DetectedDevice(display_name="device b")
    session.add_all([device, other])
    session.commit()
    mine = add_observation(session, ids, datetime(2026, 11, 9, 12, tzinfo=UTC), device.device_id)
    add_observation(session, ids, datetime(2026, 11, 9, 12, tzinfo=UTC), other.device_id)
    add_observation(session, ids, datetime(2026, 11, 9, 12, tzinfo=UTC))
    response = client.get("/observations", params={"device_id": str(device.device_id)})
    assert response.status_code == 200
    assert [o["observation_id"] for o in response.json()] == [str(mine.observation_id)]


def test_device_filter_with_no_matches_returns_empty_list(client, session, ids):
    add_observation(session, ids, datetime(2026, 11, 9, 12, tzinfo=UTC))
    response = client.get("/observations", params={"device_id": str(uuid.uuid4())})
    assert response.status_code == 200
    assert response.json() == []
