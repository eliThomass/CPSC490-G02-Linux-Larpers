import os
from functools import cache
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


@cache
def get_engine():
    return create_engine(os.environ["DATABASE_URL"])
