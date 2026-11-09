import uuid
from datetime import UTC, datetime

from sqlalchemy import JSON, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# Models with fields built from the ER diagram. 
# These models are used to create the database tables and to interact with the database.

class Base(DeclarativeBase):
    type_annotation_map = {
        datetime: DateTime(timezone=True),
        dict: JSON().with_variant(JSONB(), "postgresql"),
    }


class Scanner(Base):
    __tablename__ = "scanners"

    scanner_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str]
    hardware_model: Mapped[str]
    firmware_version: Mapped[str]
    last_connected_at: Mapped[datetime | None]


class ScanSession(Base):
    __tablename__ = "scan_sessions"

    session_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str]
    started_at: Mapped[datetime]
    ended_at: Mapped[datetime | None]
    test_conditions: Mapped[str | None]


class DetectedDevice(Base):
    __tablename__ = "detected_devices"

    device_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    display_name: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))


class Observation(Base):
    __tablename__ = "observations"

    observation_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    scanner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("scanners.scanner_id"))
    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("scan_sessions.session_id"))
    device_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("detected_devices.device_id"))
    captured_at: Mapped[datetime]
    received_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))
    protocol: Mapped[str]
    observed_address: Mapped[str | None]
    address_type: Mapped[str | None]
    rssi_dbm: Mapped[int | None]
    signal_percent: Mapped[int | None]
    metadata_: Mapped[dict] = mapped_column("metadata", default=dict)
