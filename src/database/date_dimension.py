from datetime import date, timedelta

from sqlalchemy import text

from src.utils.database import engine


def populate_dim_date(
    start_date=date(2015, 1, 1),
    end_date=date(2035, 12, 31),
):
    current_date = start_date

    query = text("""
        INSERT INTO dim_date (
            date_key,
            full_date,
            day,
            month,
            year,
            quarter,
            weekday,
            is_weekend
        )
        VALUES (
            :date_key,
            :full_date,
            :day,
            :month,
            :year,
            :quarter,
            :weekday,
            :is_weekend
        )
        ON CONFLICT (date_key)
        DO NOTHING;
    """)

    with engine.begin() as connection:
        while current_date <= end_date:

            connection.execute(
                query,
                {
                    "date_key": int(current_date.strftime("%Y%m%d")),
                    "full_date": current_date,
                    "day": current_date.day,
                    "month": current_date.month,
                    "year": current_date.year,
                    "quarter": ((current_date.month - 1) // 3) + 1,
                    "weekday": current_date.strftime("%A"),
                    "is_weekend": current_date.weekday() >= 5,
                },
            )

            current_date += timedelta(days=1)