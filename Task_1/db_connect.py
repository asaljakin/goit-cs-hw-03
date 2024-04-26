import logging
import psycopg2
from contextlib import contextmanager
from dotenv import dotenv_values

config = dotenv_values('.env')


@contextmanager
def connect():
    try:
        conn = psycopg2.connect(
            dbname=config['DB_NAME'],
            user=config['DB_USER'],
            password=config['DB_PASSWORD'],
            host=config['DB_HOST'],
            port=config['DB_PORT']
        )

        try:
            yield conn
        finally:
            conn.close()
    except psycopg2.OperationalError as e:
        logging.error(e)
