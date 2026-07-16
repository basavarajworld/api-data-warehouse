# API Data Warehouse Pipeline

A production-style Data Engineering project that extracts live data from a REST API, transforms and validates it, and loads it into a PostgreSQL data warehouse.

## Project Status

🚧 **In Progress**

### Completed

* Project structure
* Python virtual environment
* Docker & Docker Compose
* PostgreSQL setup
* Environment configuration
* Logging utility
* Database connection
* Git workflow (main / develop / feature branches)

### Upcoming

* Weather API integration
* JSON extraction
* Data transformation
* Data validation
* PostgreSQL loading
* SQL analytics
* Incremental loading
* Documentation

---

## Tech Stack

* Python 3.13
* PostgreSQL 16
* Docker
* Docker Compose
* Pandas
* SQLAlchemy
* Requests
* Psycopg2
* python-dotenv

---

## Project Structure

```text
api-data-warehouse/
│
├── src/
│   ├── main.py
│   │
│   ├── etl/
│   │   ├── extract.py
│   │   ├── transform.py
│   │   ├── validate.py
│   │   └── load.py
│   │
│   ├── services/
│   │
│   ├── models/
│   │
│   └── utils/
│       ├── database.py
│       └── logger.py
│
├── sql/
│   ├── schema.sql
│   └── analysis.sql
│
├── data/
│   ├── raw/
│   └── processed/
│
├── logs/
├── tests/
│
├── config.py
├── docker-compose.yml
├── requirements.txt
├── .env
└── README.md
```

---

## Architecture

```text
REST API
    │
    ▼
Extract
    │
    ▼
Raw JSON Storage
    │
    ▼
Transform
    │
    ▼
Validate
    │
    ▼
Load
    │
    ▼
PostgreSQL Data Warehouse
    │
    ▼
SQL Analytics
```

---

## Getting Started

### Clone Repository

```bash
git clone <repository-url>
cd api-data-warehouse
```

### Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Start PostgreSQL

```bash
docker compose up -d
```

### Run the Pipeline

```bash
python src/main.py
```

---

## Learning Objectives

* REST API integration
* JSON processing
* ETL pipeline development
* Data validation
* PostgreSQL data warehousing
* SQL analytics
* Dockerized development
* Production-ready project structure
* Git branching strategy

---

## Roadmap

* [x] Project setup
* [x] Docker & PostgreSQL
* [x] Logger
* [x] Database connection
* [ ] API extraction
* [ ] Data transformation
* [ ] Data validation
* [ ] Data loading
* [ ] Analytics
* [ ] Incremental ETL
* [ ] Documentation

---

## Author

**Basavaraj N M**
