
CREATE TABLE IF NOT EXISTS dim_account (
    account_key BIGSERIAL PRIMARY KEY,
    github_account_id BIGINT NOT NULL UNIQUE,
    login VARCHAR(255) NOT NULL UNIQUE,
    account_type VARCHAR(20) NOT NULL
        CHECK (account_type IN ('User', 'Organization','Bot')),
    avatar_url TEXT,
    html_url TEXT,
    site_admin BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);


CREATE TABLE IF NOT EXISTS dim_repository (
    repository_key BIGSERIAL PRIMARY KEY,
    github_repo_id BIGINT NOT NULL UNIQUE,

    owner_account_key BIGINT NOT NULL,

    repo_name VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL UNIQUE,

    description TEXT,

    visibility VARCHAR(20) NOT NULL
        CHECK (visibility IN ('public', 'private', 'internal')),

    default_branch VARCHAR(100),

    primary_language VARCHAR(100),

    homepage TEXT,

    size INTEGER,

    is_fork BOOLEAN NOT NULL DEFAULT FALSE,

    is_archived BOOLEAN NOT NULL DEFAULT FALSE,

    created_at TIMESTAMP,
    updated_at TIMESTAMP,

    CONSTRAINT fk_repository_owner
        FOREIGN KEY (owner_account_key)
        REFERENCES dim_account(account_key)
);

CREATE TABLE IF NOT EXISTS dim_date (
    date_key INTEGER PRIMARY KEY,

    full_date DATE NOT NULL UNIQUE,

    day SMALLINT NOT NULL,
    month SMALLINT NOT NULL,
    year SMALLINT NOT NULL,
    quarter SMALLINT NOT NULL,

    weekday VARCHAR(20) NOT NULL,

    is_weekend BOOLEAN NOT NULL
);


CREATE TABLE IF NOT EXISTS dim_label (
    label_key BIGSERIAL PRIMARY KEY,

    github_label_id BIGINT NOT NULL UNIQUE,

    label_name VARCHAR(100) NOT NULL,

    color VARCHAR(20),

    description TEXT
);