import sqlalchemy as sa

from src.config import DB_URL

engine = sa.create_engine(DB_URL, echo=True)
