from database.connection import get_connection
from database.queries import CREATE_USER_TABLE

def initialize_database():
    with get_connection() as conn:
        conn.execute(CREATE_USER_TABLE)
        conn.commit()
