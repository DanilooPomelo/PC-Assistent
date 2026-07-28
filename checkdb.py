import os

import psycopg


database_url = os.getenv("DATABASE_URL")

if database_url is None:
    raise RuntimeError("Переменная DATABASE_URL не найдена")


with psycopg.connect(database_url) as connection:
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT current_database(), current_user;"
        )

        result = cursor.fetchone()
        print(result)