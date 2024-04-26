import logging

from db_connect import connect
from insert_status import insert_status
from insert_tasks import insert_tasks
from insert_users import insert_users

def seed():
    logging.basicConfig(level=logging.INFO)

    status_names = ['new', 'in progress', 'completed']

    insert_users_stmt = """
    INSERT INTO users (fullname, email) VALUES (%s, %s) ON CONFLICT (email) DO NOTHING;
    """
    insert_tasks_stmt = """
    INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s);
    """

    try:
        with connect() as conn:
            insert_status(conn, status_names)
            insert_users(conn, insert_users_stmt)
            insert_tasks(conn, insert_tasks_stmt)
    except RuntimeError as e:
        logging.error(e)
