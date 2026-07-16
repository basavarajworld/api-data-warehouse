from sqlalchemy import create_engine
from sqlalchemy.engine import URL

from config import DB_CONFIG


DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=DB_CONFIG["user"],
    password=DB_CONFIG["password"],
    host=DB_CONFIG["host"],
    port=DB_CONFIG["port"],
    database=DB_CONFIG["database"],
)

engine = create_engine(
    DATABASE_URL,
    echo=False,
)