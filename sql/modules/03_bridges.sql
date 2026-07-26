
CREATE TABLE IF NOT EXISTS bridge_pr_assignee (

    pr_key BIGINT NOT NULL,

    assignee_account_key BIGINT NOT NULL,

    PRIMARY KEY (pr_key, assignee_account_key),

    CONSTRAINT fk_pr_assignee_pr
        FOREIGN KEY (pr_key)
        REFERENCES fact_pull_requests(pr_key),

    CONSTRAINT fk_pr_assignee_account
        FOREIGN KEY (assignee_account_key)
        REFERENCES dim_account(account_key)
);

CREATE TABLE IF NOT EXISTS bridge_pr_reviewer (

    pr_key BIGINT NOT NULL,

    reviewer_account_key BIGINT NOT NULL,

    PRIMARY KEY (pr_key, reviewer_account_key),

    CONSTRAINT fk_pr_reviewer_pr
        FOREIGN KEY (pr_key)
        REFERENCES fact_pull_requests(pr_key),

    CONSTRAINT fk_pr_reviewer_account
        FOREIGN KEY (reviewer_account_key)
        REFERENCES dim_account(account_key)
);


CREATE TABLE IF NOT EXISTS bridge_pr_label (

    pr_key BIGINT NOT NULL,

    label_key BIGINT NOT NULL,

    PRIMARY KEY (pr_key, label_key),

    CONSTRAINT fk_pr_label_pr
        FOREIGN KEY (pr_key)
        REFERENCES fact_pull_requests(pr_key),

    CONSTRAINT fk_pr_label
        FOREIGN KEY (label_key)
        REFERENCES dim_label(label_key)
);


CREATE TABLE IF NOT EXISTS bridge_issue_assignee (

    issue_key BIGINT NOT NULL,

    assignee_account_key BIGINT NOT NULL,

    PRIMARY KEY (issue_key, assignee_account_key),

    CONSTRAINT fk_issue_assignee_issue
        FOREIGN KEY (issue_key)
        REFERENCES fact_issues(issue_key),

    CONSTRAINT fk_issue_assignee_account
        FOREIGN KEY (assignee_account_key)
        REFERENCES dim_account(account_key)
);


CREATE TABLE IF NOT EXISTS bridge_issue_label (

    issue_key BIGINT NOT NULL,

    label_key BIGINT NOT NULL,

    PRIMARY KEY (issue_key, label_key),

    CONSTRAINT fk_issue_label_issue
        FOREIGN KEY (issue_key)
        REFERENCES fact_issues(issue_key),

    CONSTRAINT fk_issue_label
        FOREIGN KEY (label_key)
        REFERENCES dim_label(label_key)
);