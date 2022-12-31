import os
from os.path import dirname, join

from dotenv import load_dotenv

basedir = os.path.abspath(dirname(dirname(__file__)))
load_dotenv(join(basedir, ".env"))

DB_URL = os.environ.get("DB_URL", "postgresql://user:password@localhost:port/dbname")
