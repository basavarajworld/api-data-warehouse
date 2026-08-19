CREATE TABLE IF NOT EXISTS etl_pipeline_metadata (
    pipeline_name VARCHAR(100) PRIMARY KEY,

    last_successful_run TIMESTAMP,

    last_run_started_at TIMESTAMP,

    last_run_completed_at TIMESTAMP,

    status VARCHAR(20) NOT NULL DEFAULT 'NEVER_RUN'
        CHECK (status IN ('NEVER_RUN', 'RUNNING', 'SUCCESS', 'FAILED')),

    records_processed INTEGER NOT NULL DEFAULT 0,

    error_message TEXT,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);