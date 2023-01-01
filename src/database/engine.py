import sqlalchemy as sa
from sqlalchemy.engine.base import Engine

from src.config import DB_URL


def create_engine(host: str = None) -> Engine:
    db_url = DB_URL.replace("localhost", host) if host else DB_URL
    return sa.create_engine(db_url, echo=True)
