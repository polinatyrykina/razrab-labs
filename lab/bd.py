import psycopg2

def get_db_connection():
    return psycopg2.connect(
        dbname="razrab-labs",
        user="polina_tyrykina_knowledge_base",
        password="123",
        host="localhost",
        port="5432",
        client_encoding="utf8"
    )

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            chat_id VARCHAR UNIQUE,
            name VARCHAR
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS operations (
            id SERIAL PRIMARY KEY,
            date DATE,
            sum NUMERIC,
            chat_id VARCHAR,
            type_operation VARCHAR
        )
    """)

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("База данных успешно инициализирована.")
