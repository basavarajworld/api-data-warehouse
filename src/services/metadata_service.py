from datetime import datetime, timezone

from sqlalchemy import text

from src.utils.database import engine


def get_last_successful_run(pipeline_name: str):
    """
    Returns the last successful extraction watermark.
    Returns None if the pipeline has never run successfully.
    """

    query = text("""
        SELECT last_successful_run
        FROM etl_pipeline_metadata
        WHERE pipeline_name = :pipeline_name
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {"pipeline_name": pipeline_name},
        ).scalar_one_or_none()

    return result


def start_pipeline_run(pipeline_name: str):
    """
    Marks a pipeline as RUNNING.
    Creates the metadata record if it does not exist.

    Returns the extraction watermark for this run.
    """

    started_at = datetime.now(timezone.utc)

    query = text("""
        INSERT INTO etl_pipeline_metadata (
            pipeline_name,
            last_run_started_at,
            status,
            updated_at
        )
        VALUES (
            :pipeline_name,
            :started_at,
            'RUNNING',
            CURRENT_TIMESTAMP
        )
        ON CONFLICT (pipeline_name)
        DO UPDATE SET
            last_run_started_at = :started_at,
            status = 'RUNNING',
            error_message = NULL,
            updated_at = CURRENT_TIMESTAMP
    """)

    with engine.begin() as connection:
        connection.execute(
            query,
            {
                "pipeline_name": pipeline_name,
                "started_at": started_at,
            },
        )

    return started_at


def mark_pipeline_success(
    pipeline_name: str,
    watermark: datetime,
    records_processed: int,
):
    """
    Marks a pipeline as successfully completed.

    The watermark represents the extraction cutoff,
    not the completion time.
    """

    completed_at = datetime.now(timezone.utc)

    query = text("""
        UPDATE etl_pipeline_metadata
        SET
            last_successful_run = :watermark,
            last_run_completed_at = :completed_at,
            status = 'SUCCESS',
            records_processed = :records_processed,
            error_message = NULL,
            updated_at = CURRENT_TIMESTAMP
        WHERE pipeline_name = :pipeline_name
    """)

    with engine.begin() as connection:
        connection.execute(
            query,
            {
                "pipeline_name": pipeline_name,
                "watermark": watermark,
                "completed_at": completed_at,
                "records_processed": records_processed,
            },
        )


def mark_pipeline_failed(
    pipeline_name: str,
    error_message: str,
):
    """
    Marks a pipeline as failed without advancing
    the last successful watermark.
    """

    query = text("""
        UPDATE etl_pipeline_metadata
        SET
            status = 'FAILED',
            error_message = :error_message,
            updated_at = CURRENT_TIMESTAMP
        WHERE pipeline_name = :pipeline_name
    """)

    with engine.begin() as connection:
        connection.execute(
            query,
            {
                "pipeline_name": pipeline_name,
                "error_message": error_message,
            },
        )