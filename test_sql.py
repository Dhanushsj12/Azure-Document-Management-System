import pyodbc

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=documentmanagementdb.database.windows.net;"
    "DATABASE=documentmanagementdb;"
    "UID=sqladmin;"
    "PWD=Document@12345;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
)

print("Connected Successfully!")

conn.close()