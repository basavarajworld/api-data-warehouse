from pathlib import Path

from sqlalchemy import text

from src.utils.database import engine
from src.utils.logger import get_logger

logger = get_logger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent.parent

MODULES_DIR = BASE_DIR / "sql" / "modules"

DROP_SCHEMA_FILE = BASE_DIR / "sql" / "drop_schema.sql"

SQL_FILES = sorted(MODULES_DIR.glob("*.sql"))


def execute_sql_file(connection, sql_file: Path) -> None:
    """
    Executes a single SQL file.
    """

    logger.info(f"Executing {sql_file.name}")

    query = sql_file.read_text(encoding="utf-8")

    connection.execute(text(query))


def create_schema() -> None:
    """
    Creates the complete warehouse schema.
    """

    logger.info("Creating warehouse schema...")

    try:
        with engine.begin() as connection:

            for sql_file in SQL_FILES:
                execute_sql_file(connection, sql_file)

        logger.info("Warehouse schema created successfully.")

    except Exception:
        logger.exception("Failed to create warehouse schema.")
        raise


def drop_schema() -> None:
    """
    Drops the complete warehouse schema.
    """

    logger.info("Dropping warehouse schema...")

    try:
        with engine.begin() as connection:

            execute_sql_file(connection, DROP_SCHEMA_FILE)

        logger.info("Warehouse schema dropped successfully.")

    except Exception:
        logger.exception("Failed to drop warehouse schema.")
        raise


def reset_schema() -> None:
    """
    Drops and recreates the warehouse schema.
    """

    logger.info("Resetting warehouse schema...")

    drop_schema()

    create_schema()

    logger.info("Warehouse schema reset completed.")