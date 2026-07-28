from fastapi import FastAPI

from backend.database import check_database


app = FastAPI(title="PC Assistant API")


@app.get("/")
def root():
    return {"message": "PC Assistant API работает"}


@app.get("/db-check")
def db_check():
    database_name, database_user = check_database()

    return {
        "database": database_name,
        "user": database_user,
        "status": "connected",
    }