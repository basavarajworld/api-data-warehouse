from datetime import datetime

from src.utils.logger import get_logger

logger = get_logger(__name__)


def transform_account(account: dict) -> dict:
    """
    Transform GitHub account into dim_account format.
    """

    logger.info("Transforming account...")

    return {
        "github_account_id": account["id"],
        "login": account["login"],
        "account_type": account["type"],
        "avatar_url": account["avatar_url"],
        "html_url": account["html_url"],
        "site_admin": account["site_admin"],
        "created_at": None,
        "updated_at": None,
    }


def transform_repository(repository: dict) -> dict:
    logger.info("Transforming repository...")

    return {
        "github_repo_id": repository["id"],
        "owner_github_account_id": repository["owner"]["id"],
        "repo_name": repository["name"],
        "full_name": repository["full_name"],
        "description": repository["description"],
        "visibility": repository["visibility"],
        "default_branch": repository["default_branch"],
        "primary_language": repository["language"],
        "homepage": repository["homepage"],
        "size": repository["size"],
        "is_fork": repository["fork"],
        "is_archived": repository["archived"],
        "created_at": repository["created_at"],
        "updated_at": repository["updated_at"],
    }


def transform_commit(commit: dict, github_repo_id: int) -> dict:
    """
    Transform GitHub commit into fact_commits format.
    """

    logger.info("Transforming commit...")

    commit_timestamp = commit["commit"]["committer"]["date"]

    date_key = int(
        datetime.fromisoformat(
            commit_timestamp.replace("Z", "+00:00")
        ).strftime("%Y%m%d")
    )

    return {
        "commit_sha": commit["sha"],
        "github_repo_id": github_repo_id,
        "author_github_account_id": (
            commit["author"]["id"]
            if commit["author"]
            else None
        ),
        "committer_github_account_id": (
            commit["committer"]["id"]
            if commit["committer"]
            else None
        ),
        "date_key": date_key,
        "commit_timestamp": commit_timestamp,
        "commit_message": commit["commit"]["message"],
        "is_verified": commit["commit"]["verification"]["verified"],
    }


def transform_pull_request(pr, github_repo_id):
    """
    Transform GitHub pull request JSON into warehouse format.
    """

    def get_date_key(timestamp):
        if timestamp is None:
            return None

        return int(
            datetime.fromisoformat(
                timestamp.replace("Z", "+00:00")
            ).strftime("%Y%m%d")
        )

    return {
        "github_pr_id": pr["id"],
        "pr_number": pr["number"],

        "github_repo_id": github_repo_id,

        "author_github_account_id": (
            pr["user"]["id"]
            if pr.get("user")
            else None
        ),

        "created_date_key": get_date_key(pr["created_at"]),
        "closed_date_key": get_date_key(pr["closed_at"]),
        "merged_date_key": get_date_key(pr["merged_at"]),

        "created_at": datetime.fromisoformat(
            pr["created_at"].replace("Z", "+00:00")
        ),

        "updated_at": datetime.fromisoformat(
            pr["updated_at"].replace("Z", "+00:00")
        ),

        "closed_at": (
            datetime.fromisoformat(
                pr["closed_at"].replace("Z", "+00:00")
            )
            if pr["closed_at"]
            else None
        ),

        "merged_at": (
            datetime.fromisoformat(
                pr["merged_at"].replace("Z", "+00:00")
            )
            if pr["merged_at"]
            else None
        ),

        "state": pr["state"],
        "draft": pr["draft"],
        "merged": pr["merged"],

        "title": pr["title"],

        "comments_count": pr["comments"],
        "review_comments_count": pr["review_comments"],

        "commits_count": pr["commits"],

        "additions": pr["additions"],
        "deletions": pr["deletions"],
        "changed_files": pr["changed_files"],

        "source_branch": pr["head"]["ref"],
        "target_branch": pr["base"]["ref"],

        "merge_commit_sha": pr["merge_commit_sha"],
    }


def transform_review(review: dict, github_pr_id: int) -> dict:
    """
    Transform GitHub review into warehouse format.
    """

    logger.info("Transforming review...")

    submitted_at = datetime.fromisoformat(
        review["submitted_at"].replace("Z", "+00:00")
    )

    submitted_date_key = int(
        submitted_at.strftime("%Y%m%d")
    )

    return {
        "github_review_id": review["id"],

        "github_pr_id": github_pr_id,

        "reviewer_github_account_id": (
            review["user"]["id"]
            if review.get("user")
            else None
        ),

        "submitted_date_key": submitted_date_key,
        "submitted_at": submitted_at,

        "state": review["state"],

        "commit_id": review["commit_id"],

        "body": review["body"],
    }


def transform_issue(issue: dict, github_repo_id: int) -> dict:
    """
    Transform GitHub issue into warehouse format.
    """

    logger.info("Transforming issue...")

    created_at = datetime.fromisoformat(
        issue["created_at"].replace("Z", "+00:00")
    )

    updated_at = datetime.fromisoformat(
        issue["updated_at"].replace("Z", "+00:00")
    )

    closed_at = (
        datetime.fromisoformat(
            issue["closed_at"].replace("Z", "+00:00")
        )
        if issue.get("closed_at")
        else None
    )

    return {
        "github_issue_id": issue["id"],
        "issue_number": issue["number"],

        "github_repo_id": github_repo_id,

        "author_github_account_id": (
            issue["user"]["id"]
            if issue.get("user")
            else None
        ),

        "created_date_key": int(
            created_at.strftime("%Y%m%d")
        ),

        "updated_date_key": int(
            updated_at.strftime("%Y%m%d")
        ),

        "closed_date_key": (
            int(closed_at.strftime("%Y%m%d"))
            if closed_at
            else None
        ),

        "created_at": created_at,
        "updated_at": updated_at,
        "closed_at": closed_at,

        "state": issue["state"],

        "title": issue["title"],

        "comments_count": issue["comments"],
    }

def transform_label(label: dict) -> dict:
    return {
        "github_label_id": label["id"],
        "label_name": label["name"],
        "color": label["color"],
        "description": label.get("description"),
    }

def transform_pr_assignee(pr_assignee: dict) -> dict:
    """
    Transform PR assignee.
    """

    logger.info("Transforming PR assignee...")

    return {
        "github_pr_id": pr_assignee["github_pr_id"],
        "github_account_id": pr_assignee["assignee"]["id"],
    }

def transform_pr_reviewer(pr_reviewer):
    return {
        "github_pr_id": pr_reviewer["github_pr_id"],
        "github_account_id": pr_reviewer["reviewer"]["id"],
    }

def transform_pr_label(pr_label):

    return {
        "github_pr_id": pr_label["github_pr_id"],
        "github_label_id": pr_label["label"]["id"],
    }

def transform_issue_assignee(issue_assignee):

    return {
        "github_issue_id": issue_assignee["github_issue_id"],
        "github_account_id": issue_assignee["assignee"]["id"],
    }

def transform_issue_label(issue_label):

    return {
        "github_issue_id": issue_label["github_issue_id"],
        "github_label_id": issue_label["label"]["id"],
    }