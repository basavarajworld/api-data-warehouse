import requests

from config import (
    GITHUB_API_BASE_URL,
    GITHUB_TOKEN,
    REQUEST_TIMEOUT,
)
from src.utils.logger import get_logger

logger = get_logger(__name__)


def build_headers() -> dict:
    """
    Build HTTP headers for GitHub API requests.
    """

    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    return headers


def make_request(endpoint: str, params: dict | None = None):
    """
    Generic GET request to GitHub API.
    """

    url = f"{GITHUB_API_BASE_URL}{endpoint}"

    logger.info("Requesting %s", url)

    try:
        response = requests.get(
            url,
            headers=build_headers(),
            params=params,
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        logger.info("Request completed successfully.")

        return response.json()

    except requests.RequestException as error:
        logger.error("GitHub API request failed: %s", error)
        raise


def get_repository(owner: str, repo: str) -> dict:
    return make_request(f"/repos/{owner}/{repo}")


def get_commits(owner: str, repo: str) -> list:
    return make_request(f"/repos/{owner}/{repo}/commits")


def get_issues(owner: str, repo: str) -> list:
    return make_request(f"/repos/{owner}/{repo}/issues")


def get_pull_requests(owner: str, repo: str) -> list:
    return make_request(f"/repos/{owner}/{repo}/pulls")


def get_contributors(owner: str, repo: str) -> list:
    return make_request(f"/repos/{owner}/{repo}/contributors")


def get_languages(owner: str, repo: str) -> dict:
    return make_request(f"/repos/{owner}/{repo}/languages")


def get_releases(owner: str, repo: str) -> list:
    return make_request(f"/repos/{owner}/{repo}/releases")

def get_pull_request_details(owner: str, repo: str, pull_number: int) -> dict:
    return make_request(f"/repos/{owner}/{repo}/pulls/{pull_number}")


def get_reviews(owner: str, repo: str, pull_number: int) -> list:
    return make_request(f"/repos/{owner}/{repo}/pulls/{pull_number}/reviews")

def get_pull_request(owner: str, repository: str, pull_number: int):
    endpoint = f"/repos/{owner}/{repository}/pulls/{pull_number}"

    return make_request(endpoint)

def get_issues(owner: str, repo: str) -> list:
    """
    Fetch all issues for a repository.
    Pull requests are excluded.
    """

    endpoint = f"/repos/{owner}/{repo}/issues"

    params = {
        "state": "all",
        "per_page": 100,
    }

    issues = make_request(endpoint, params=params)

    return [
        issue
        for issue in issues
        if "pull_request" not in issue
    ]