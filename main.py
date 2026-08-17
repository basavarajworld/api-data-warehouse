from src.database.date_dimension import populate_dim_date

from src.etl.extract import (
    extract_issue_assignees,
    extract_issue_labels,
    extract_issues,
    extract_labels,
    extract_pr_assignees,
    extract_pr_labels,
    extract_pr_reviewers,
    extract_pull_request,
    extract_repository,
    extract_commits,
    extract_pull_requests,
    extract_reviews,
)

from src.etl.transform import (
    transform_account,
    transform_issue,
    transform_issue_assignee,
    transform_issue_label,
    transform_label,
    transform_pr_assignee,
    transform_pr_label,
    transform_pr_reviewer,
    transform_repository,
    transform_commit,
    transform_pull_request,
    transform_review,
)

from src.etl.load import (
    ensure_account_exists,
    load_account,
    load_issue,
    load_issue_assignee,
    load_issue_label,
    load_label,
    load_pr_assignee,
    load_pr_label,
    load_pr_reviewer,
    load_repository,
    load_commit,
    load_pull_request,
    load_repository_daily_metrics,
    load_review,
)

from src.services.metadata_service import (
    get_last_successful_run,
    start_pipeline_run,
    mark_pipeline_success,
    mark_pipeline_failed,
)


OWNER = "microsoft"
REPOSITORY = "vscode"


def main():

    # Run only when creating/resetting the warehouse
    # create_schema()

    # Populate Date Dimension
    populate_dim_date()

    # ============================================================
    # Repository
    # ============================================================

    repository = extract_repository(
        OWNER,
        REPOSITORY,
    )

    account = transform_account(
        repository["owner"]
    )

    load_account(account)

    repository_data = transform_repository(
        repository
    )

    load_repository(repository_data)

    print("✅ Repository ETL completed.")

    # ============================================================
    # Commits - Incremental Load
    # ============================================================

    pipeline_name = "commits"

    last_run = get_last_successful_run(
        pipeline_name
    )

    watermark = start_pipeline_run(
        pipeline_name
    )

    try:

        commits = extract_commits(
            OWNER,
            REPOSITORY,
            since=last_run,
        )

        for commit in commits:

            ensure_account_exists(
                commit["author"]
            )

            ensure_account_exists(
                commit["committer"]
            )

            commit_data = transform_commit(
                commit,
                repository["id"],
            )

            load_commit(commit_data)

        mark_pipeline_success(
            pipeline_name,
            watermark,
            len(commits),
        )

        print(
            f"✅ Commit ETL completed. "
            f"{len(commits)} commits processed."
        )

    except Exception as error:

        mark_pipeline_failed(
            pipeline_name,
            str(error),
        )

        raise

    # ============================================================
    # Pull Requests
    # ============================================================

    pull_requests = extract_pull_requests(
        OWNER,
        REPOSITORY,
    )

    for pr in pull_requests:

        # Get complete PR details
        pr = extract_pull_request(
            OWNER,
            REPOSITORY,
            pr["number"],
        )

        ensure_account_exists(
            pr["user"]
        )

        pr_data = transform_pull_request(
            pr,
            repository["id"],
        )

        load_pull_request(pr_data)

    print("✅ Pull Request ETL completed.")

    # ============================================================
    # Labels
    # ============================================================

    labels = extract_labels(
        pull_requests
    )

    for label in labels:

        transformed_label = transform_label(
            label
        )

        load_label(
            transformed_label
        )

    # ============================================================
    # Reviews
    # ============================================================

    all_reviews = []

    for pr in pull_requests:

        full_pr = extract_pull_request(
            OWNER,
            REPOSITORY,
            pr["number"],
        )

        reviews = extract_reviews(
            OWNER,
            REPOSITORY,
            pr["number"],
        )

        for review in reviews:

            all_reviews.append(
                {
                    "github_pr_id": full_pr["id"],
                    "review": review,
                }
            )

            if review.get("user"):

                ensure_account_exists(
                    review["user"]
                )

            transformed_review = transform_review(
                review,
                full_pr["id"],
            )

            load_review(
                transformed_review
            )

    print("✅ Review ETL completed.")

    # ============================================================
    # Issues
    # ============================================================

    issues = extract_issues(
        owner=OWNER,
        repo=REPOSITORY,
    )

    for issue in issues:

        if issue.get("user"):

            ensure_account_exists(
                issue["user"]
            )

        transformed_issue = transform_issue(
            issue,
            repository["id"],
        )

        load_issue(
            transformed_issue
        )

    print("✅ Issue ETL completed.")

    # ============================================================
    # Issue Labels
    # ============================================================

    labels = extract_labels(
        issues
    )

    for label in labels:

        transformed_label = transform_label(
            label
        )

        load_label(
            transformed_label
        )

    # ============================================================
    # Bridge PR Assignees
    # ============================================================

    pr_assignees = extract_pr_assignees(
        pull_requests
    )

    for pr_assignee in pr_assignees:

        transformed_account = transform_account(
            pr_assignee["assignee"]
        )

        load_account(
            transformed_account
        )

        transformed_pr_assignee = (
            transform_pr_assignee(
                pr_assignee
            )
        )

        load_pr_assignee(
            transformed_pr_assignee
        )

    # ============================================================
    # Bridge PR Labels
    # ============================================================

    pr_labels = extract_pr_labels(
        pull_requests
    )

    for pr_label in pr_labels:

        transformed_label = transform_label(
            pr_label["label"]
        )

        load_label(
            transformed_label
        )

        transformed = transform_pr_label(
            pr_label
        )

        load_pr_label(
            transformed
        )

    # ============================================================
    # Bridge PR Reviewers
    # ============================================================

    pr_reviewers = extract_pr_reviewers(
        all_reviews
    )

    for pr_reviewer in pr_reviewers:

        transformed_account = transform_account(
            pr_reviewer["reviewer"]
        )

        load_account(
            transformed_account
        )

        transformed = transform_pr_reviewer(
            pr_reviewer
        )

        load_pr_reviewer(
            transformed
        )

    # ============================================================
    # Bridge Issue Assignees
    # ============================================================

    issue_assignees = extract_issue_assignees(
        issues
    )

    for issue_assignee in issue_assignees:

        transformed_account = transform_account(
            issue_assignee["assignee"]
        )

        load_account(
            transformed_account
        )

        transformed = transform_issue_assignee(
            issue_assignee
        )

        load_issue_assignee(
            transformed
        )

    # ============================================================
    # Bridge Issue Labels
    # ============================================================

    issue_labels = extract_issue_labels(
        issues
    )

    for issue_label in issue_labels:

        transformed_label = transform_label(
            issue_label["label"]
        )

        load_label(
            transformed_label
        )

        transformed = transform_issue_label(
            issue_label
        )

        load_issue_label(
            transformed
        )

    # ============================================================
    # Repository Daily Metrics
    # ============================================================

    load_repository_daily_metrics()

    print(
        "🎉 GitHub Engineering Analytics ETL "
        "completed successfully."
    )


if __name__ == "__main__":
    main()