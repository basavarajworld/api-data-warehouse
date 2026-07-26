from src.services.github_service import (
    get_pull_request,
    get_repository,
    get_commits,
    get_issues,
    get_pull_requests,
    get_pull_request_details,
    get_reviews,
    get_contributors,
    get_languages,
    get_releases,
)
from src.utils.logger import get_logger

logger = get_logger(__name__)


def extract_repository(owner: str, repo: str) -> dict:
    """Extract repository details."""

    logger.info("Extracting repository...")
    return get_repository(owner, repo)


def extract_commits(owner: str, repo: str) -> list:
    """Extract repository commits."""

    logger.info("Extracting commits...")
    return get_commits(owner, repo)


def extract_issues(owner: str, repo: str) -> list:
    """Extract repository issues."""

    logger.info("Extracting issues...")
    return get_issues(owner, repo)


def extract_pull_requests(owner: str, repo: str) -> list:
    """Extract repository pull requests."""

    logger.info("Extracting pull requests...")
    return get_pull_requests(owner, repo)

def extract_pull_request(owner, repository, pull_number):
    return get_pull_request(
        owner,
        repository,
        pull_number,
    )


def extract_pull_request_details(owner: str, repo: str, pull_number: int) -> dict:
    """Extract detailed information for a pull request."""

    logger.info("Extracting pull request #%s...", pull_number)
    return get_pull_request_details(owner, repo, pull_number)


def extract_reviews(owner: str, repo: str, pull_number: int) -> list:
    """Extract pull request reviews."""

    logger.info("Extracting reviews for pull request #%s...", pull_number)
    return get_reviews(owner, repo, pull_number)


def extract_contributors(owner: str, repo: str) -> list:
    """Extract repository contributors."""

    logger.info("Extracting contributors...")
    return get_contributors(owner, repo)


def extract_languages(owner: str, repo: str) -> dict:
    """Extract repository language statistics."""

    logger.info("Extracting languages...")
    return get_languages(owner, repo)


def extract_releases(owner: str, repo: str) -> list:
    """Extract repository releases."""

    logger.info("Extracting releases...")
    return get_releases(owner, repo)

def extract_issues(owner: str, repo: str) -> list:
    """
    Extract issues from GitHub.
    """

    logger.info("Extracting issues...")

    return get_issues(owner, repo)

def extract_labels(items: list) -> list:
    """
    Extract labels from pull requests or issues.
    """

    logger.info("Extracting labels...")

    labels = []

    for item in items:
        labels.extend(item.get("labels", []))

    return labels

def extract_pr_assignees(pull_requests):

    assignees = []

    for pr in pull_requests:

        for assignee in pr.get("assignees", []):

            assignees.append(
                {
                    "github_pr_id": pr["id"],
                    "assignee": assignee
                }
            )

    return assignees

def extract_pr_reviewers(reviews):

    reviewers = []

    for item in reviews:

        if item["review"].get("user"):

            reviewers.append({
                "github_pr_id": item["github_pr_id"],
                "reviewer": item["review"]["user"]
            })

    return reviewers

def extract_pr_labels(pull_requests):

    labels = []

    for pr in pull_requests:
        for label in pr.get("labels", []):

            labels.append({
                "github_pr_id": pr["id"],
                "label": label
            })

    return labels

def extract_issue_assignees(issues):

    assignees = []

    for issue in issues:
        for assignee in issue.get("assignees", []):

            assignees.append({
                "github_issue_id": issue["id"],
                "assignee": assignee,
            })

    return assignees

def extract_issue_labels(issues):

    labels = []

    for issue in issues:
        for label in issue.get("labels", []):

            labels.append({
                "github_issue_id": issue["id"],
                "label": label,
            })

    return labels