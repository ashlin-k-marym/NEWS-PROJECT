import psycopg2

conn = psycopg2.connect(
    host="database-host",
    database="new_db",
    user="postgres",
    password="password",
    port="5432"
)

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS news_data (
    id SERIAL PRIMARY KEY,
    title TEXT,
    description TEXT,
    sentiment VARCHAR(20),
    published_at TIMESTAMP
)
""")

conn.commit()

print("Table created successfully!")

cur.close()
conn.close()