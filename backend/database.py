import os

import psycopg


def check_database() -> tuple[str, str]:
    database_url = os.getenv("DATABASE_URL")

    if database_url is None:
        raise RuntimeError("Переменная DATABASE_URL не найдена")

    with psycopg.connect(database_url) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT current_database(), current_user;"
            )

            result = cursor.fetchone()

    if result is None:
        raise RuntimeError("PostgreSQL не вернул результат")

    database_name, database_user = result

    return database_name, database_user