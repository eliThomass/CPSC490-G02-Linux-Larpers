import os
from functools import cache
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models import Base

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


@cache
def get_engine():
    engine = create_engine(os.environ["DATABASE_URL"])
    Base.metadata.create_all(engine)
    return engine


def get_session():
    with Session(get_engine()) as session:
        yield session
