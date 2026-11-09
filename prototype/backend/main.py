from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from db import get_engine, get_session
from models import DetectedDevice, Observation, ScanSession, Scanner
from schemas import ObservationCreate

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
