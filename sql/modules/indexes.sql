
-- ==========================================
-- FACT COMMITS
-- ==========================================

CREATE INDEX IF NOT EXISTS idx_commits_repository
ON fact_commits(repository_key);

CREATE INDEX IF NOT EXISTS idx_commits_author
ON fact_commits(author_account_key);

CREATE INDEX IF NOT EXISTS idx_commits_committer
ON fact_commits(committer_account_key);

CREATE INDEX IF NOT EXISTS idx_commits_date
ON fact_commits(date_key);

-- ==========================================
-- FACT PULL REQUESTS
-- ==========================================

CREATE INDEX IF NOT EXISTS idx_pr_repository
ON fact_pull_requests(repository_key);

CREATE INDEX IF NOT EXISTS idx_pr_author
ON fact_pull_requests(author_account_key);

CREATE INDEX IF NOT EXISTS idx_pr_created_date
ON fact_pull_requests(created_date_key);

CREATE INDEX IF NOT EXISTS idx_pr_closed_date
ON fact_pull_requests(closed_date_key);

CREATE INDEX IF NOT EXISTS idx_pr_merged_date
ON fact_pull_requests(merged_date_key);

-- ==========================================
-- FACT ISSUES
-- ==========================================

CREATE INDEX IF NOT EXISTS idx_issue_repository
ON fact_issues(repository_key);

CREATE INDEX IF NOT EXISTS idx_issue_author
ON fact_issues(author_account_key);

CREATE INDEX IF NOT EXISTS idx_issue_created_date
ON fact_issues(created_date_key);

CREATE INDEX IF NOT EXISTS idx_issue_closed_date
ON fact_issues(closed_date_key);

-- ==========================================
-- FACT REVIEWS
-- ==========================================

CREATE INDEX IF NOT EXISTS idx_review_pr
ON fact_reviews(pr_key);

CREATE INDEX IF NOT EXISTS idx_review_account
ON fact_reviews(reviewer_account_key);

CREATE INDEX IF NOT EXISTS idx_review_date
ON fact_reviews(submitted_date_key);

-- ==========================================
-- DAILY METRICS
-- ==========================================

CREATE INDEX IF NOT EXISTS idx_metrics_repository
ON fact_repository_daily_metrics(repository_key);

CREATE INDEX IF NOT EXISTS idx_metrics_date
ON fact_repository_daily_metrics(date_key);

-- ==========================================
-- BRIDGE TABLES
-- ==========================================

CREATE INDEX IF NOT EXISTS idx_pr_assignee_account
ON bridge_pr_assignee(assignee_account_key);

CREATE INDEX IF NOT EXISTS idx_pr_reviewer_account
ON bridge_pr_reviewer(reviewer_account_key);

CREATE INDEX IF NOT EXISTS idx_pr_label
ON bridge_pr_label(label_key);

-- CREATE INDEX IF NOT EXISTS idx_issue_assignee_account
-- ON bridge_issue_assignee(assignee_account_key);

-- CREATE INDEX IF NOT EXISTS idx_issue_label
-- ON bridge_issue_label(label_key);