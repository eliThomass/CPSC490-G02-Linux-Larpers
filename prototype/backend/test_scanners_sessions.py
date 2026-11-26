import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from db import get_session
from main import app
from models import Base, ScanSession, Scanner


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


SCANNER = {"name": "node-1", "hardware_model": "ESP32", "firmware_version": "0.1.0"}


def test_scanner_is_registered(client, session):
    response = client.post("/scanners", json=SCANNER)
    assert response.status_code == 201
    row = session.get(Scanner, uuid.UUID(response.json()["scanner_id"]))
    assert (row.name, row.hardware_model, row.firmware_version) == ("node-1", "ESP32", "0.1.0")


@pytest.mark.parametrize("body", [
    {"name": "node-1", "hardware_model": "ESP32"},
    {**SCANNER, "name": ""},
])
def test_invalid_scanner_is_rejected(client, session, body):
    response = client.post("/scanners", json=body)
    assert response.status_code == 422
    assert session.scalars(select(Scanner)).all() == []


def test_session_is_started(client, session):
    response = client.post("/sessions", json={"name": "lab test", "test_conditions": "1 m, idle"})
    assert response.status_code == 201
    row = session.get(ScanSession, uuid.UUID(response.json()["session_id"]))
    assert row.name == "lab test"
    assert row.test_conditions == "1 m, idle"
    assert row.started_at is not None
    assert row.ended_at is None


def test_invalid_session_is_rejected(client, session):
    response = client.post("/sessions", json={"test_conditions": "1 m, idle"})
    assert response.status_code == 422
    assert session.scalars(select(ScanSession)).all() == []


def test_session_is_ended(client, session):
    session_id = client.post("/sessions", json={"name": "lab test"}).json()["session_id"]
    response = client.post(f"/sessions/{session_id}/end")
    assert response.status_code == 200
    assert session.get(ScanSession, uuid.UUID(session_id)).ended_at is not None


def test_ending_unknown_session_is_rejected(client):
    response = client.post(f"/sessions/{uuid.uuid4()}/end")
    assert response.status_code == 404


def test_ending_session_twice_is_rejected(client):
    session_id = client.post("/sessions", json={"name": "lab test"}).json()["session_id"]
    client.post(f"/sessions/{session_id}/end")
    response = client.post(f"/sessions/{session_id}/end")
    assert response.status_code == 409


def test_new_scanner_and_session_accept_observations(client):
    scanner_id = client.post("/scanners", json=SCANNER).json()["scanner_id"]
    session_id = client.post("/sessions", json={"name": "lab test"}).json()["session_id"]
    response = client.post("/observations", json={
        "scanner_id": scanner_id,
        "session_id": session_id,
        "captured_at": "2026-11-26T12:00:00Z",
        "protocol": "wifi",
    })
    assert response.status_code == 201
