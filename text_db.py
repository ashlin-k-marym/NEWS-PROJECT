import psycopg2

conn = psycopg2.connect(
    host="database-host",
    database="new_db",
    user="postgres",
    password="password",
    port="5432"
)

cur = conn.cursor()