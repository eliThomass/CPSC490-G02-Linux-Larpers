from typing import Literal
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, Field

# Will check all incoming observations for validity and reject any that are invalid. 
# This is to prevent bad data from being stored in the database.
class ObservationCreate(BaseModel):
    scanner_id: UUID
    session_id: UUID
    device_id: UUID | None = None
    captured_at: AwareDatetime
    protocol: Literal["wifi", "bluetooth"]
    observed_address: str | None = None
    address_type: str | None = None
    rssi_dbm: int | None = None
    signal_percent: int | None = Field(default=None, ge=0, le=100)
    metadata: dict = {}
