
CREATE TABLE IF NOT EXISTS fact_commits (
    commit_key BIGSERIAL PRIMARY KEY,

    commit_sha VARCHAR(40) NOT NULL UNIQUE,

    repository_key BIGINT NOT NULL,
    author_account_key BIGINT,
    committer_account_key BIGINT,
    date_key INTEGER NOT NULL,

    commit_timestamp TIMESTAMP NOT NULL,

    commit_message TEXT NOT NULL,

    is_verified BOOLEAN NOT NULL DEFAULT FALSE,

    CONSTRAINT fk_commit_repository
        FOREIGN KEY (repository_key)
        REFERENCES dim_repository(repository_key),

    CONSTRAINT fk_commit_author
        FOREIGN KEY (author_account_key)
        REFERENCES dim_account(account_key),

    CONSTRAINT fk_commit_committer
        FOREIGN KEY (committer_account_key)
        REFERENCES dim_account(account_key),

    CONSTRAINT fk_commit_date
        FOREIGN KEY (date_key)
        REFERENCES dim_date(date_key)
);

CREATE TABLE IF NOT EXISTS fact_pull_requests (
    pr_key BIGSERIAL PRIMARY KEY,

    github_pr_id BIGINT NOT NULL UNIQUE,
    pr_number INTEGER NOT NULL,

    repository_key BIGINT NOT NULL,
    author_account_key BIGINT,

    created_date_key INTEGER NOT NULL,
    closed_date_key INTEGER,
    merged_date_key INTEGER,
    updated_at TIMESTAMP NOT NULL,

    created_at TIMESTAMP NOT NULL,
    closed_at TIMESTAMP,
    source_branch VARCHAR(255),
    merge_commit_sha VARCHAR(40),
    target_branch VARCHAR(255),
    merged_at TIMESTAMP,

    state VARCHAR(20) NOT NULL
        CHECK (state IN ('open', 'closed')),

    draft BOOLEAN NOT NULL DEFAULT FALSE,

    title TEXT NOT NULL,

    comments_count INTEGER NOT NULL DEFAULT 0,
    review_comments_count INTEGER NOT NULL DEFAULT 0,

    commits_count INTEGER NOT NULL DEFAULT 0,

    additions INTEGER NOT NULL DEFAULT 0,
    deletions INTEGER NOT NULL DEFAULT 0,
    changed_files INTEGER NOT NULL DEFAULT 0,

    merged BOOLEAN NOT NULL DEFAULT FALSE,

    CONSTRAINT fk_pr_repository
        FOREIGN KEY (repository_key)
        REFERENCES dim_repository(repository_key),

    CONSTRAINT fk_pr_author
        FOREIGN KEY (author_account_key)
        REFERENCES dim_account(account_key),

    CONSTRAINT fk_pr_created_date
        FOREIGN KEY (created_date_key)
        REFERENCES dim_date(date_key),

    CONSTRAINT fk_pr_closed_date
        FOREIGN KEY (closed_date_key)
        REFERENCES dim_date(date_key),

    CONSTRAINT fk_pr_merged_date
        FOREIGN KEY (merged_date_key)
        REFERENCES dim_date(date_key)
);

CREATE TABLE if not exists fact_issues (
    issue_key BIGSERIAL PRIMARY KEY,

    github_issue_id BIGINT NOT NULL UNIQUE,
    issue_number INTEGER,

    repository_key BIGINT NOT NULL,
    author_account_key BIGINT,

    created_date_key INTEGER NOT NULL,
    updated_date_key INTEGER NOT NULL,
    closed_date_key INTEGER,

    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    closed_at TIMESTAMP,

    state VARCHAR(20) NOT NULL
        CHECK (state IN ('open', 'closed')),

    title TEXT NOT NULL,

    comments_count INTEGER NOT NULL DEFAULT 0,

    CONSTRAINT fk_issue_repository
        FOREIGN KEY (repository_key)
        REFERENCES dim_repository(repository_key),

    CONSTRAINT fk_issue_author
        FOREIGN KEY (author_account_key)
        REFERENCES dim_account(account_key),

    CONSTRAINT fk_issue_created_date
        FOREIGN KEY (created_date_key)
        REFERENCES dim_date(date_key),

    CONSTRAINT fk_issue_updated_date
        FOREIGN KEY (updated_date_key)
        REFERENCES dim_date(date_key),

    CONSTRAINT fk_issue_closed_date
        FOREIGN KEY (closed_date_key)
        REFERENCES dim_date(date_key)
);

CREATE TABLE if not exists fact_reviews (
    review_key BIGSERIAL PRIMARY KEY,

    github_review_id BIGINT NOT NULL UNIQUE,

    pr_key BIGINT NOT NULL,

    reviewer_account_key BIGINT,

    submitted_date_key INTEGER NOT NULL,

    submitted_at TIMESTAMP NOT NULL,
    commit_id VARCHAR(40),
    body TEXT,

    state VARCHAR(30) NOT NULL,

    CONSTRAINT fk_review_pr
        FOREIGN KEY (pr_key)
        REFERENCES fact_pull_requests(pr_key),

    CONSTRAINT fk_review_account
        FOREIGN KEY (reviewer_account_key)
        REFERENCES dim_account(account_key),

    CONSTRAINT fk_review_date
        FOREIGN KEY (submitted_date_key)
        REFERENCES dim_date(date_key)
);


CREATE TABLE IF NOT EXISTS fact_repository_daily_metrics (

    metric_key BIGSERIAL PRIMARY KEY,

    repository_key BIGINT NOT NULL,
    date_key INTEGER NOT NULL,

    commit_count INTEGER NOT NULL DEFAULT 0,
    pull_request_count INTEGER NOT NULL DEFAULT 0,
    merged_pr_count INTEGER NOT NULL DEFAULT 0,
    review_count INTEGER NOT NULL DEFAULT 0,
    issue_count INTEGER NOT NULL DEFAULT 0,
    open_issue_count INTEGER NOT NULL DEFAULT 0,
    closed_issue_count INTEGER NOT NULL DEFAULT 0,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_metrics_repository
        FOREIGN KEY (repository_key)
        REFERENCES dim_repository(repository_key),

    CONSTRAINT fk_metrics_date
        FOREIGN KEY (date_key)
        REFERENCES dim_date(date_key),

    CONSTRAINT uq_repository_date
        UNIQUE(repository_key, date_key)
);