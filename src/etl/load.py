from sqlalchemy import text
from src.etl.transform import transform_account
from src.utils.database import (
    engine,
    fetch_one,
)
from src.utils.logger import get_logger

logger = get_logger(__name__)


def load_account(account: dict) -> None:
    """
    Insert account into dim_account.
    """

    logger.info("Loading account...")

    query = """
    INSERT INTO dim_account (
        github_account_id,
        login,
        account_type,
        avatar_url,
        html_url,
        site_admin,
        created_at,
        updated_at
    )
    VALUES (
        :github_account_id,
        :login,
        :account_type,
        :avatar_url,
        :html_url,
        :site_admin,
        :created_at,
        :updated_at
    )
    ON CONFLICT (github_account_id)
    DO NOTHING;
    """

    with engine.begin() as connection:
        connection.execute(text(query), account)


def get_account_key(github_account_id: int) -> int:
    """
    Return surrogate account key.
    """

    query = """
    SELECT account_key
    FROM dim_account
    WHERE github_account_id = :github_account_id;
    """

    return fetch_one(
        query,
        {
            "github_account_id": github_account_id
        },
    )


def load_repository(repository: dict) -> None:
    """
    Insert repository into dim_repository.
    """

    logger.info("Loading repository...")

    owner_account_key = get_account_key(
        repository["owner_github_account_id"]
    )

    query = """
    INSERT INTO dim_repository (
        github_repo_id,
        owner_account_key,
        repo_name,
        full_name,
        description,
        visibility,
        default_branch,
        primary_language,
        homepage,
        size,
        is_fork,
        is_archived,
        created_at,
        updated_at
    )
    VALUES (
        :github_repo_id,
        :owner_account_key,
        :repo_name,
        :full_name,
        :description,
        :visibility,
        :default_branch,
        :primary_language,
        :homepage,
        :size,
        :is_fork,
        :is_archived,
        :created_at,
        :updated_at
    )
    ON CONFLICT (github_repo_id)
    DO NOTHING;
    """

    repository = repository.copy()
    repository["owner_account_key"] = owner_account_key
    repository.pop("owner_github_account_id")

    with engine.begin() as connection:
        connection.execute(text(query), repository)


def ensure_account_exists(account: dict | None) -> None:
    """
    Load GitHub account into dim_account if it doesn't already exist.
    """

    if account is None:
        return

    transformed_account = transform_account(account)
    load_account(transformed_account)        


def get_repository_key(github_repo_id: int) -> int:
    """
    Return surrogate repository key.
    """

    query = """
    SELECT repository_key
    FROM dim_repository
    WHERE github_repo_id = :github_repo_id;
    """

    return fetch_one(
        query,
        {
            "github_repo_id": github_repo_id
        },
    )

def get_date_key(date_key: int) -> int:
    """
    Return surrogate date key.
    """

    query = """
    SELECT date_key
    FROM dim_date
    WHERE date_key = :date_key;
    """

    return fetch_one(
        query,
        {
            "date_key": date_key
        },
    )


def load_commit(commit: dict) -> None:
    """
    Insert commit into fact_commits.
    """

    logger.info("Loading commit...")

    repository_key = get_repository_key(
        commit["github_repo_id"]
    )

    author_account_key = (
        get_account_key(commit["author_github_account_id"])
        if commit["author_github_account_id"]
        else None
    )

    committer_account_key = (
        get_account_key(commit["committer_github_account_id"])
        if commit["committer_github_account_id"]
        else None
    )

    commit = commit.copy()

    commit["repository_key"] = repository_key
    commit["author_account_key"] = author_account_key
    commit["committer_account_key"] = committer_account_key

    commit.pop("github_repo_id")
    commit.pop("author_github_account_id")
    commit.pop("committer_github_account_id")

    query = """
    INSERT INTO fact_commits (
        commit_sha,
        repository_key,
        author_account_key,
        committer_account_key,
        date_key,
        commit_timestamp,
        commit_message,
        is_verified
    )
    VALUES (
        :commit_sha,
        :repository_key,
        :author_account_key,
        :committer_account_key,
        :date_key,
        :commit_timestamp,
        :commit_message,
        :is_verified
    )
    ON CONFLICT (commit_sha)
    DO NOTHING;
    """

    with engine.begin() as connection:
        connection.execute(text(query), commit)



def load_pull_request(pr):
    """
    Load transformed pull request into fact_pull_requests.
    """

    repository_key = get_repository_key(pr["github_repo_id"])

    author_account_key = get_account_key(
        pr["author_github_account_id"]
    )

    query = """
        INSERT INTO fact_pull_requests (
            github_pr_id,
            pr_number,

            repository_key,
            author_account_key,

            created_date_key,
            closed_date_key,
            merged_date_key,

            created_at,
            updated_at,
            closed_at,
            merged_at,

            state,
            draft,
            merged,

            title,

            comments_count,
            review_comments_count,
            commits_count,

            additions,
            deletions,
            changed_files,

            source_branch,
            target_branch,

            merge_commit_sha
        )
        VALUES (
            :github_pr_id,
            :pr_number,

            :repository_key,
            :author_account_key,

            :created_date_key,
            :closed_date_key,
            :merged_date_key,

            :created_at,
            :updated_at,
            :closed_at,
            :merged_at,

            :state,
            :draft,
            :merged,

            :title,

            :comments_count,
            :review_comments_count,
            :commits_count,

            :additions,
            :deletions,
            :changed_files,

            :source_branch,
            :target_branch,

            :merge_commit_sha
        )
        ON CONFLICT (github_pr_id)
        DO NOTHING;
    """

    values = pr.copy()

    values["repository_key"] = repository_key
    values["author_account_key"] = author_account_key

    values.pop("github_repo_id")
    values.pop("author_github_account_id")

    with engine.begin() as connection:
        connection.execute(text(query), values)        


def load_review(review: dict) -> None:
    """
    Load a review into fact_reviews.
    """

    logger.info("Loading review...")

    with engine.begin() as connection:

        # Resolve Pull Request surrogate key
        pr_key = connection.execute(
            text("""
                SELECT pr_key
                FROM fact_pull_requests
                WHERE github_pr_id = :github_pr_id
            """),
            {
                "github_pr_id": review["github_pr_id"]
            },
        ).scalar()

        # Resolve Reviewer surrogate key
        reviewer_account_key = get_account_key(
            review["reviewer_github_account_id"]
        )

        values = {
            **review,
            "pr_key": pr_key,
            "reviewer_account_key": reviewer_account_key,
        }

        query = """
        INSERT INTO fact_reviews (

            github_review_id,

            pr_key,
            reviewer_account_key,

            submitted_date_key,
            submitted_at,

            state,

            commit_id,

            body

        )
        VALUES (

            :github_review_id,

            :pr_key,
            :reviewer_account_key,

            :submitted_date_key,
            :submitted_at,

            :state,

            :commit_id,

            :body

        )
        ON CONFLICT (github_review_id)
        DO NOTHING;
        """

        connection.execute(text(query), values)   


def load_issue(issue: dict) -> None:

    logger.info("Loading issue...")

    with engine.begin() as connection:

        repository_key = get_repository_key(
            issue["github_repo_id"]
        )

        author_account_key = get_account_key(
            issue["author_github_account_id"]
        )

        values = {
            **issue,
            "repository_key": repository_key,
            "author_account_key": author_account_key,
        }

        query = """
        INSERT INTO fact_issues (

            github_issue_id,

            repository_key,
            author_account_key,

            created_date_key,
            updated_date_key,
            closed_date_key,

            created_at,
            updated_at,
            closed_at,

            state,

            title,

            comments_count

        )
        VALUES (

            :github_issue_id,

            :repository_key,
            :author_account_key,

            :created_date_key,
            :updated_date_key,
            :closed_date_key,

            :created_at,
            :updated_at,
            :closed_at,

            :state,

            :title,

            :comments_count

        )
        ON CONFLICT (github_issue_id)
        DO NOTHING;
        """

        connection.execute(text(query), values)  


def load_label(label: dict):
    """
    Load label into dim_label.
    """

    logger.info("Loading label...")

    query = """
        INSERT INTO dim_label
        (  
            github_label_id,
            label_name,
            color,
            description
        )
        VALUES
        (
            :github_label_id,
            :label_name,
            :color,
            :description
        )
        ON CONFLICT (github_label_id)
        DO NOTHING;
        """

    with engine.begin() as connection:
        connection.execute(text(query), label)   


def get_pr_key(github_pr_id: int):
    """
    Get warehouse PR key.
    """

    query = """
        SELECT pr_key
        FROM fact_pull_requests
        WHERE github_pr_id = :github_pr_id;
    """

    with engine.begin() as conn:
        result = conn.execute(
            text(query),
            {"github_pr_id": github_pr_id},
        ).fetchone()

    return result[0] if result else None

def load_pr_assignee(pr_assignee: dict):
    """
    Load PR assignee bridge.
    """

    logger.info("Loading PR assignee...")

    pr_key = get_pr_key(
        pr_assignee["github_pr_id"]
    )

    assignee_account_key = get_account_key(
        pr_assignee["github_account_id"]
    )

    if pr_key is None:
        logger.warning(
            f"PR not found: {pr_assignee['github_pr_id']}"
        )
        return

    if assignee_account_key is None:
        logger.warning(
            f"Assignee not found: {pr_assignee['github_account_id']}"
        )
        return

    logger.info(
        f"Loading bridge: pr_key={pr_key}, "
        f"assignee_account_key={assignee_account_key}"
    )

    query = """
        INSERT INTO bridge_pr_assignee
        (
            pr_key,
            assignee_account_key
        )
        VALUES
        (
            :pr_key,
            :assignee_account_key
        )
        ON CONFLICT
        DO NOTHING;
    """

    with engine.begin() as conn:
        conn.execute(
            text(query),
            {
                "pr_key": pr_key,
                "assignee_account_key": assignee_account_key,
            },
        )

def get_label_key(github_label_id: int):
    """
    Get warehouse label key.
    """

    query = """
        SELECT label_key
        FROM dim_label
        WHERE github_label_id = :github_label_id;
    """

    with engine.begin() as conn:
        result = conn.execute(
            text(query),
            {
                "github_label_id": github_label_id,
            },
        ).fetchone()

    return result[0] if result else None

def load_pr_reviewer(pr_reviewer: dict):
    """
    Load PR reviewer bridge.
    """

    logger.info("Loading PR reviewer...")

    pr_key = get_pr_key(
        pr_reviewer["github_pr_id"]
    )

    reviewer_account_key = get_account_key(
        pr_reviewer["github_account_id"]
    )

    if pr_key is None:
        logger.warning(
            f"PR not found: {pr_reviewer['github_pr_id']}"
        )
        return

    if reviewer_account_key is None:
        logger.warning(
            f"Reviewer not found: {pr_reviewer['github_account_id']}"
        )
        return

    query = """
        INSERT INTO bridge_pr_reviewer
        (
            pr_key,
            reviewer_account_key
        )
        VALUES
        (
            :pr_key,
            :reviewer_account_key
        )
        ON CONFLICT
        DO NOTHING;
    """

    with engine.begin() as conn:
        conn.execute(
            text(query),
            {
                "pr_key": pr_key,
                "reviewer_account_key": reviewer_account_key,
            },
        )


def load_pr_label(pr_label: dict):
    """
    Load PR label bridge.
    """

    logger.info("Loading PR label...")

    pr_key = get_pr_key(
        pr_label["github_pr_id"]
    )

    label_key = get_label_key(
        pr_label["github_label_id"]
    )

    if pr_key is None:
        logger.warning(
            f"PR not found: {pr_label['github_pr_id']}"
        )
        return

    if label_key is None:
        logger.warning(
            f"Label not found: {pr_label['github_label_id']}"
        )
        return

    query = """
        INSERT INTO bridge_pr_label
        (
            pr_key,
            label_key
        )
        VALUES
        (
            :pr_key,
            :label_key
        )
        ON CONFLICT
        DO NOTHING;
    """

    with engine.begin() as conn:
        conn.execute(
            text(query),
            {
                "pr_key": pr_key,
                "label_key": label_key,
            },
        )

def get_issue_key(github_issue_id: int):
    """
    Get warehouse issue key.
    """

    query = """
        SELECT issue_key
        FROM fact_issues
        WHERE github_issue_id = :github_issue_id;
    """

    with engine.begin() as conn:
        result = conn.execute(
            text(query),
            {
                "github_issue_id": github_issue_id,
            },
        ).fetchone()

    return result[0] if result else None

def load_issue_assignee(issue_assignee: dict):
    """
    Load Issue Assignee bridge.
    """

    logger.info("Loading Issue Assignee...")

    issue_key = get_issue_key(
        issue_assignee["github_issue_id"]
    )

    assignee_account_key = get_account_key(
        issue_assignee["github_account_id"]
    )

    if issue_key is None:
        logger.warning(
            f"Issue not found: {issue_assignee['github_issue_id']}"
        )
        return

    if assignee_account_key is None:
        logger.warning(
            f"Assignee not found: {issue_assignee['github_account_id']}"
        )
        return

    query = """
        INSERT INTO bridge_issue_assignee
        (
            issue_key,
            assignee_account_key
        )
        VALUES
        (
            :issue_key,
            :assignee_account_key
        )
        ON CONFLICT DO NOTHING;
    """

    with engine.begin() as conn:
        conn.execute(
            text(query),
            {
                "issue_key": issue_key,
                "assignee_account_key": assignee_account_key,
            },
        )    


def load_issue_label(issue_label: dict):
    """
    Load Issue Label bridge.
    """

    logger.info("Loading Issue Label...")

    issue_key = get_issue_key(
        issue_label["github_issue_id"]
    )

    label_key = get_label_key(
        issue_label["github_label_id"]
    )

    if issue_key is None:
        logger.warning(
            f"Issue not found: {issue_label['github_issue_id']}"
        )
        return

    if label_key is None:
        logger.warning(
            f"Label not found: {issue_label['github_label_id']}"
        )
        return

    query = """
        INSERT INTO bridge_issue_label
        (
            issue_key,
            label_key
        )
        VALUES
        (
            :issue_key,
            :label_key
        )
        ON CONFLICT DO NOTHING;
    """

    with engine.begin() as conn:
        conn.execute(
            text(query),
            {
                "issue_key": issue_key,
                "label_key": label_key,
            },
        )            

def load_repository_daily_metrics():
    """
    Populate repository daily metrics from warehouse fact tables.
    """

    logger.info("Loading repository daily metrics...")

    query = """
    WITH activity_dates AS (

        SELECT repository_key, date_key
        FROM fact_commits

        UNION

        SELECT repository_key, created_date_key
        FROM fact_pull_requests

        UNION

        SELECT
            p.repository_key,
            r.submitted_date_key
        FROM fact_reviews r
        JOIN fact_pull_requests p
            ON r.pr_key = p.pr_key

        UNION

        SELECT repository_key, created_date_key
        FROM fact_issues
    )

    INSERT INTO fact_repository_daily_metrics
    (
        repository_key,
        date_key,
        commit_count,
        pull_request_count,
        merged_pr_count,
        review_count,
        issue_count,
        open_issue_count,
        closed_issue_count
    )

    SELECT

        ad.repository_key,
        ad.date_key,

        COALESCE(c.commit_count, 0),
        COALESCE(pr.pr_count, 0),
        COALESCE(pr.merged_pr_count, 0),
        COALESCE(rv.review_count, 0),
        COALESCE(i.issue_count, 0),
        COALESCE(i.open_issue_count, 0),
        COALESCE(i.closed_issue_count, 0)

    FROM activity_dates ad

    LEFT JOIN
    (
        SELECT
            repository_key,
            date_key,
            COUNT(*) AS commit_count
        FROM fact_commits
        GROUP BY repository_key, date_key
    ) c
        ON c.repository_key = ad.repository_key
       AND c.date_key = ad.date_key

    LEFT JOIN
    (
        SELECT
            repository_key,
            created_date_key AS date_key,
            COUNT(*) AS pr_count,
            SUM(
                CASE
                    WHEN merged THEN 1
                    ELSE 0
                END
            ) AS merged_pr_count
        FROM fact_pull_requests
        GROUP BY repository_key, created_date_key
    ) pr
        ON pr.repository_key = ad.repository_key
       AND pr.date_key = ad.date_key

    LEFT JOIN
    (
        SELECT
            p.repository_key,
            r.submitted_date_key AS date_key,
            COUNT(*) AS review_count
        FROM fact_reviews r
        JOIN fact_pull_requests p
            ON r.pr_key = p.pr_key
        GROUP BY
            p.repository_key,
            r.submitted_date_key
    ) rv
        ON rv.repository_key = ad.repository_key
       AND rv.date_key = ad.date_key

    LEFT JOIN
    (
        SELECT
            repository_key,
            created_date_key AS date_key,

            COUNT(*) AS issue_count,

            SUM(
                CASE
                    WHEN state = 'open'
                    THEN 1
                    ELSE 0
                END
            ) AS open_issue_count,

            SUM(
                CASE
                    WHEN state = 'closed'
                    THEN 1
                    ELSE 0
                END
            ) AS closed_issue_count

        FROM fact_issues

        GROUP BY
            repository_key,
            created_date_key
    ) i
        ON i.repository_key = ad.repository_key
       AND i.date_key = ad.date_key

    ON CONFLICT (repository_key, date_key)
    DO NOTHING;
    """

    with engine.begin() as conn:
        conn.execute(text(query))

    logger.info("Repository daily metrics loaded.")        