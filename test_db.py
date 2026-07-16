from config import DB_CONFIG

print(DB_CONFIG)

from sqlalchemy import text
from src.utils.database import engine

with engine.connect() as connection:
    result = connection.execute(text("SELECT current_database();"))
    print(result.fetchone())