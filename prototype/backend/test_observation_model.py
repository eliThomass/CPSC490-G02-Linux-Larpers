import uuid
from datetime import UTC, datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import Base, DetectedDevice, Observation, ScanSession, Scanner


@pytest.fixture
def session():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    engine.dispose()


@pytest.fixture
def required_fields(session):
    scanner = Scanner(name="node-1", hardware_model="ESP32", firmware_version="0.1.0")
    scan_session = ScanSession(name="test", started_at=datetime.now(UTC))
    session.add_all([scanner, scan_session])
    session.commit()
    return {
        "scanner_id": scanner.scanner_id,
        "session_id": scan_session.session_id,
        "captured_at": datetime(2026, 11, 9, 12, tzinfo=UTC),
        "protocol": "wifi",
    }


@pytest.mark.parametrize("protocol, address_type, metadata", [
    ("wifi", "bssid", {"ssid": "test-network", "channel": 6}),
    ("bluetooth", "random", {"local_name": "test-device"}),
])
def test_complete_record_is_accepted(session, required_fields, protocol, address_type, metadata):
    device = DetectedDevice(display_name="test device")
    session.add(device)
    session.commit()
    row = Observation(**{
        **required_fields,
        "protocol": protocol,
        "device_id": device.device_id,
        "observed_address": "aa:bb:cc:dd:ee:ff",
        "address_type": address_type,
        "rssi_dbm": -60,
        "signal_percent": 80,
        "metadata_": metadata,
    })
    session.add(row)
    session.commit()
    session.refresh(row)

    assert isinstance(row.observation_id, uuid.UUID)
    assert isinstance(row.received_at, datetime)
    assert row.scanner_id == required_fields["scanner_id"]
    assert row.session_id == required_fields["session_id"]
    assert row.captured_at.replace(tzinfo=UTC) == required_fields["captured_at"]
    assert row.protocol == protocol
    assert row.device_id == device.device_id
    assert row.observed_address == "aa:bb:cc:dd:ee:ff"
    assert row.address_type == address_type
    assert row.rssi_dbm == -60
    assert row.signal_percent == 80
    assert row.metadata_ == metadata


@pytest.mark.parametrize("protocol", ["wifi", "bluetooth"])
def test_partial_record_has_unavailable_fields(session, required_fields, protocol):
    row = Observation(**{**required_fields, "protocol": protocol})
    session.add(row)
    session.commit()
    session.refresh(row)

    assert row.protocol == protocol
    assert row.device_id is None
    assert row.observed_address is None
    assert row.address_type is None
    assert row.rssi_dbm is None
    assert row.signal_percent is None
    assert row.metadata_ == {}


@pytest.mark.parametrize("missing_field", ["scanner_id", "session_id", "captured_at", "protocol"])
def test_missing_required_field_is_rejected(session, required_fields, missing_field):
    del required_fields[missing_field]
    session.add(Observation(**required_fields))

    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()
    assert session.query(Observation).count() == 0
