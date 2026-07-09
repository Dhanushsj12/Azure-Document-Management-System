import os
from urllib.parse import quote_plus

from dotenv import load_dotenv

load_dotenv()


class Config:

    SECRET_KEY = os.getenv("SECRET_KEY")

    # Azure SQL Database Connection
    username = os.getenv("SQL_USERNAME")
    password = quote_plus(os.getenv("SQL_PASSWORD"))
    server = os.getenv("SQL_SERVER")
    database = os.getenv("SQL_DATABASE")

    SQLALCHEMY_DATABASE_URI = (
        f"mssql+pyodbc://{username}:{password}"
        f"@{server}:1433/{database}"
        "?driver=ODBC+Driver+18+for+SQL+Server"
        "&Encrypt=yes"
        "&TrustServerCertificate=no"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False