import sqlalchemy as sa
from sqlalchemy.engine.base import Engine
from src.config import DB_URL


def create_engine(host: str = None) -> Engine:
    if host:
        db_url = DB_URL.replace("localhost", host).replace("port", "5432")
    else:
        db_url = DB_URL.replace("port", "5433")
    return sa.create_engine(db_url, echo=True)
