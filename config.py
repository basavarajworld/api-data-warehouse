import os

from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

GITHUB_API_BASE_URL = "https://api.github.com"

REQUEST_TIMEOUT = 10