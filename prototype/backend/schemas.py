from typing import Literal
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, Field


# Will check all incoming observations for validity and reject any that are invalid.
# This is to prevent bad data from being stored in the database.
class ObservationCreate(BaseModel):
    scanner_id: UUID = Field(description="ID of the scanner that captured the signal.")
    session_id: UUID = Field(description="ID of the collection or testing period.")
    device_id: UUID | None = Field(
        default=None,
        description="Tracked device ID, if already associated with this capture.",
    )
    captured_at: AwareDatetime = Field(
        description="Address observed in the capture; (Not permanent device id)"
    )
    protocol: Literal["wifi", "bluetooth"]
    observed_address: str | None = None
    address_type: str | None = Field(
        default=None, description="Type of observed address, if available (ex, bssid)"
    )
    rssi_dbm: int | None = Field(
        default=None,
        description="Received signal strength in dBm, if available. Not percentage",
    )
    signal_percent: int | None = Field(
        default=None,
        ge=0,
        le=100,
        description="Signal percentage (0-100), if supplied by the source. Not converted from RSSI",
    )
    metadata: dict = Field(
        default_factory=dict,
        description="Additional capture metadata, empty obj if unavailable",
    )
