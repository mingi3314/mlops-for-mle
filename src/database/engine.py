import sqlalchemy as sa
from sqlalchemy.engine.base import Engine

from src.config import DB_URL


def create_engine(host: str = None) -> Engine:
    if host:
        DB_URL.replace("localhost", host)
    return sa.create_engine(DB_URL, echo=True)
