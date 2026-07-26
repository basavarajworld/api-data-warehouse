# GitHub Engineering Analytics Platform

A production-style **Data Engineering** project that extracts engineering data from the GitHub REST API, transforms it into a dimensional data warehouse, and enables analytics on repositories, commits, pull requests, reviews, issues, and engineering productivity.

---

# Project Overview

This project demonstrates the complete lifecycle of a modern ETL pipeline:

* Extract data from the GitHub REST API
* Clean and transform nested JSON data
* Load into a PostgreSQL dimensional warehouse
* Build analytical fact and dimension tables
* Generate repository-level engineering metrics

The warehouse is designed using **Star Schema** principles and supports historical analytics through surrogate keys, bridge tables, and aggregated fact tables.

---

# Tech Stack

| Category         | Technology         |
| ---------------- | ------------------ |
| Language         | Python 3           |
| Database         | PostgreSQL         |
| ETL              | Python, SQLAlchemy |
| API              | GitHub REST API    |
| Data Processing  | Pandas             |
| Containerization | Docker             |
| Version Control  | Git & GitHub       |

---

# Project Structure

```text
api-data-warehouse/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── sql/
│   ├── schema/
│   └── queries/
│
├── src/
│   ├── etl/
│   │   ├── extract.py
│   │   ├── transform.py
│   │   └── load.py
│   │
│   ├── services/
│   │   └── github_service.py
│   │
│   └── utils/
│       ├── database.py
│       └── logger.py
│
├── main.py
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# Data Warehouse Architecture

## Dimension Tables

* dim_date
* dim_account
* dim_repository
* dim_label

---

## Fact Tables

* fact_commits
* fact_pull_requests
* fact_reviews
* fact_issues
* fact_repository_daily_metrics

---

## Bridge Tables

* bridge_pr_assignee
* bridge_pr_reviewer
* bridge_pr_label
* bridge_issue_assignee
* bridge_issue_label

---

# ETL Workflow

```text
GitHub REST API
        │
        ▼
Extract
        │
        ▼
Transform
        │
        ▼
Load
        │
        ▼
PostgreSQL Data Warehouse
        │
        ▼
Analytics
```

---

# Data Pipeline

The pipeline performs the following steps:

1. Extract repository information
2. Extract commits
3. Extract pull requests
4. Extract pull request reviews
5. Extract issues
6. Transform nested API responses
7. Resolve surrogate keys
8. Load dimension tables
9. Load fact tables
10. Load bridge tables
11. Generate repository daily metrics

---

# Warehouse Design

The warehouse follows dimensional modelling principles.

### Dimensions

Dimensions store descriptive business entities.

* Repository
* GitHub Account
* Date
* Label

### Facts

Facts capture engineering events.

* Commit activity
* Pull request activity
* Review activity
* Issue activity

### Bridge Tables

Bridge tables resolve many-to-many relationships between entities.

Examples:

* Pull Request ↔ Reviewer
* Pull Request ↔ Assignee
* Pull Request ↔ Label
* Issue ↔ Assignee
* Issue ↔ Label

---

# Repository Daily Metrics

The warehouse generates an aggregated metrics table with one row per repository per day.

Metrics include:

* Commit Count
* Pull Request Count
* Merged Pull Request Count
* Review Count
* Issue Count
* Open Issue Count
* Closed Issue Count

This table enables fast dashboard reporting without repeatedly aggregating raw event data.

---

# Features

* Modular ETL architecture
* Production-style project structure
* Dimensional Data Warehouse
* Surrogate Keys
* Foreign Key Relationships
* Many-to-Many Bridge Tables
* Aggregated Fact Table
* Dockerized PostgreSQL
* SQLAlchemy Integration
* Structured Logging
* Incremental Key Resolution

---

# Running the Project

## Clone Repository

```bash
git clone <repository-url>
cd api-data-warehouse
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Start PostgreSQL

```bash
docker compose up -d
```

## Configure Environment

Create a `.env` file:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=github_dw
DB_USER=postgres
DB_PASSWORD=your_password

GITHUB_TOKEN=your_github_token
```

## Execute

```bash
python main.py
```

---

# Example Analytics

The warehouse can answer questions such as:

* How many commits are made each day?
* Which contributors are the most active?
* Which repositories receive the most pull requests?
* Pull request merge trends
* Repository review activity
* Daily engineering productivity
* Issue creation and closure trends
* Contributor activity over time
* Label usage across repositories

---

# Learning Outcomes

This project demonstrates practical experience with:

* ETL Pipeline Development
* REST API Integration
* Data Warehouse Design
* Star Schema Modelling
* PostgreSQL
* SQLAlchemy
* Docker
* Python
* GitHub REST API
* Dimensional Modelling
* Data Engineering Best Practices

---

# Future Improvements

* Incremental API extraction
* GitHub GraphQL API support
* Apache Airflow orchestration
* Data quality validation framework
* Automated testing
* CI/CD pipeline
* Power BI / Tableau dashboards
* Cloud deployment (AWS, Azure or GCP)

---

# License

This project is licensed under the MIT License.
