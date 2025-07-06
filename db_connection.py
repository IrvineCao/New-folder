import singlestoredb as s2
from contextlib import contextmanager
import json
# Kết nối toàn cục
conn = None

def load_config():
    with open('config.json') as f:
        return json.load(f)

def open_connection():
    global conn
    if conn is None:  # Nếu chưa kết nối, mở kết nối
        config = load_config()
        conn = s2.connect(
            host=config['db_host'],
            port=config['db_port'],
            user=config['db_user'],
            password=config['db_password'],
            database=config['db_name']
        )
        print("Database connection established.")
    return conn


def close_connection():
    global conn
    if conn is not None:  # Nếu kết nối đang mở, đóng kết nối
        conn.close()
        conn = None
        print("Database connection closed.")

@contextmanager
def get_connection():
    """Context manager for database connection handling"""
    conn = open_connection()
    try:
        yield conn
    finally:
        pass