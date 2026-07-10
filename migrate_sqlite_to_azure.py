import sqlite3
import pyodbc
from datetime import datetime

# ---------- SQLite ----------
sqlite_conn = sqlite3.connect("instance/document_management.db")
sqlite_conn.row_factory = sqlite3.Row
sqlite_cur = sqlite_conn.cursor()

# ---------- Azure SQL ----------
azure_conn = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=documentmanagementdb.database.windows.net;"
    "DATABASE=documentmanagementdb;"
    "UID=sqladmin;"
    "PWD=Document@12345;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
)
azure_cur = azure_conn.cursor()

tables = [
    "users",
    "documents",
    "versions",
    "audits"
]

for table in tables:

    print(f"\n========== {table.upper()} ==========")

    sqlite_cur.execute(f"SELECT * FROM {table}")
    rows = sqlite_cur.fetchall()

    if len(rows) == 0:
        print("No rows found.")
        continue

    columns = rows[0].keys()

    column_string = ",".join(columns)
    placeholders = ",".join(["?"] * len(columns))

    # Enable identity insert
    azure_cur.execute(f"SET IDENTITY_INSERT {table} ON")

    insert_sql = f"""
    INSERT INTO {table} ({column_string})
    VALUES ({placeholders})
    """

    copied = 0

    for row in rows:

        values = []

        for value in row:

            # Convert SQLite datetime string to Python datetime
            if isinstance(value, str):
                try:
                    value = datetime.fromisoformat(value)
                except ValueError:
                    pass

            values.append(value)

        azure_cur.execute(insert_sql, values)
        copied += 1

    azure_conn.commit()

    azure_cur.execute(f"SET IDENTITY_INSERT {table} OFF")
    azure_conn.commit()

    print(f"Copied {copied} rows.")

sqlite_conn.close()
azure_conn.close()

print("\n====================================")
print("Migration Completed Successfully!")
print("====================================")