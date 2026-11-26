from datetime import UTC, datetime
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException
from pydantic import AwareDatetime
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from db import get_engine, get_session
from models import DetectedDevice, Observation, ScanSession, Scanner
from schemas import ObservationCreate, ObservationRead, ScanSessionCreate, ScannerCreate

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/health/db")
def health_db():
    with get_engine().connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"database": "ok"}

@app.post("/observations", status_code=201)
def create_observation(observation: ObservationCreate, session: Session = Depends(get_session)):
    if session.get(Scanner, observation.scanner_id) is None:
        raise HTTPException(422, f"Unknown scanner_id: {observation.scanner_id}")
    if session.get(ScanSession, observation.session_id) is None:
        raise HTTPException(422, f"Unknown session_id: {observation.session_id}")
    if observation.device_id and session.get(DetectedDevice, observation.device_id) is None:
        raise HTTPException(422, f"Unknown device_id: {observation.device_id}")
    data = observation.model_dump()
    data["metadata_"] = data.pop("metadata")
    row = Observation(**data)
    session.add(row)
    session.commit()
    return {"observation_id": row.observation_id, "received_at": row.received_at}

@app.get("/observations", response_model=list[ObservationRead])
def list_observations(
    start: AwareDatetime | None = None,
    end: AwareDatetime | None = None,
    device_id: UUID | None = None,
    session: Session = Depends(get_session),
):
    query = select(Observation).order_by(Observation.captured_at)
    if start:
        query = query.where(Observation.captured_at >= start)
    if end:
        query = query.where(Observation.captured_at <= end)
    if device_id:
        query = query.where(Observation.device_id == device_id)
    return session.scalars(query).all()


@app.post("/scanners", status_code=201)
def create_scanner(scanner: ScannerCreate, session: Session = Depends(get_session)):
    row = Scanner(**scanner.model_dump())
    session.add(row)
    session.commit()
    return {"scanner_id": row.scanner_id}


@app.post("/sessions", status_code=201)
def start_session(scan_session: ScanSessionCreate, session: Session = Depends(get_session)):
    row = ScanSession(**scan_session.model_dump(), started_at=datetime.now(UTC))
    session.add(row)
    session.commit()
    return {"session_id": row.session_id, "started_at": row.started_at}


@app.post("/sessions/{session_id}/end")
def end_session(session_id: UUID, session: Session = Depends(get_session)):
    row = session.get(ScanSession, session_id)
    if row is None:
        raise HTTPException(404, f"Unknown session_id: {session_id}")
    if row.ended_at is not None:
        raise HTTPException(409, f"Session already ended: {session_id}")
    row.ended_at = datetime.now(UTC)
    session.commit()
    return {"session_id": row.session_id, "ended_at": row.ended_at}
