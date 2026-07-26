from typing import Any

from sqlalchemy import text, create_engine
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


def execute_query(query: str, params: dict | None = None) -> None:
    """
    Execute INSERT/UPDATE/DELETE statements.
    """
    with engine.begin() as connection:
        connection.execute(text(query), params or {})


def fetch_one(query: str, params: dict | None = None) -> Any:
    """
    Execute a query and return a single scalar value.
    """
    with engine.begin() as connection:
        return connection.execute(
            text(query),
            params or {},
        ).scalar()


def fetch_row(query: str, params: dict | None = None):
    """
    Return one complete row.
    """
    with engine.begin() as connection:
        return connection.execute(
            text(query),
            params or {},
        ).mappings().first()


def fetch_all(query: str, params: dict | None = None):
    """
    Return all rows.
    """
    with engine.begin() as connection:
        return connection.execute(
            text(query),
            params or {},
        ).mappings().all()