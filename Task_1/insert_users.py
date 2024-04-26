import logging
from psycopg2 import DatabaseError
from faker import Faker

fake = Faker('uk_UA')
COUNT = 10

def insert_users(conn, sql_stmt: str):
    cursor = conn.cursor()
    try:
        for _ in range(COUNT):
            fullname = fake.name()
            email = fake.email()
            cursor.execute(sql_stmt, (fullname, email))
        conn.commit()
    except DatabaseError as e:
        logging.error(e)
        conn.rollback()
    finally:
        cursor.close()
