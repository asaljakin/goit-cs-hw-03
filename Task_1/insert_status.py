import logging
from psycopg2 import DatabaseError

def insert_status(conn, status_names):
    cursor = conn.cursor()
    try:
        for name in status_names:
            cursor.execute("INSERT INTO status (name) VALUES (%s) ON CONFLICT DO NOTHING;", (name,))

        conn.commit()
    except DatabaseError as e:
        logging.error(e)
        conn.rollback()
    finally:
        cursor.close()
