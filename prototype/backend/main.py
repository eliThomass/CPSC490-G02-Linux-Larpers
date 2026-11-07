from fastapi import FastAPI
from sqlalchemy import text

from db import get_engine

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
