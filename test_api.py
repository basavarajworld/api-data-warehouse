from pprint import pprint

from src.services.github_service import (
    get_repository,
    get_commits,
    get_contributors,
    get_issues,
    get_pull_requests,
    get_languages,
    get_releases,
)


OWNER = "apache"
REPO = "spark"


def section(title: str):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


# ==========================================================
# Repository
# ==========================================================
section("REPOSITORY")

repository = get_repository(OWNER, REPO)

print(type(repository))
print(f"Total Fields: {len(repository)}")
pprint(repository)


# ==========================================================
# Contributors
# ==========================================================
section("CONTRIBUTORS")

contributors = get_contributors(OWNER, REPO)

print(type(contributors))
print(f"Total Contributors Returned: {len(contributors)}")

if contributors:
    pprint(contributors[0])


# ==========================================================
# Commits
# ==========================================================
section("COMMITS")

commits = get_commits(OWNER, REPO)

print(type(commits))
print(f"Total Commits Returned: {len(commits)}")

if commits:
    pprint(commits[0])


# ==========================================================
# Issues
# ==========================================================
section("ISSUES")

issues = get_issues(OWNER, REPO)

print(type(issues))
print(f"Total Issues Returned: {len(issues)}")

if issues:
    pprint(issues[0])


# ==========================================================
# Pull Requests
# ==========================================================
section("PULL REQUESTS")

pull_requests = get_pull_requests(OWNER, REPO)

print(type(pull_requests))
print(f"Total Pull Requests Returned: {len(pull_requests)}")

if pull_requests:
    pprint(pull_requests[0])


# ==========================================================
# Languages
# ==========================================================
section("LANGUAGES")

languages = get_languages(OWNER, REPO)

print(type(languages))
pprint(languages)


# ==========================================================
# Releases
# ==========================================================
section("RELEASES")

releases = get_releases(OWNER, REPO)

print(type(releases))
print(f"Total Releases Returned: {len(releases)}")

if releases:
    pprint(releases[0])