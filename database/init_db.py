from database.connection import get_connection
from database.queries import CREATE_USER_TABLE, CREATE_SCOOTER_TABLE, CREATE_TRAVELLERS_TABLE, CREATE_RESTORE_CODE_TABLE

def initialize_database():
    with get_connection() as conn:
        conn.execute(CREATE_USER_TABLE)
        conn.execute(CREATE_SCOOTER_TABLE)
        conn.execute(CREATE_TRAVELLERS_TABLE)
        conn.execute(CREATE_RESTORE_CODE_TABLE)
        conn.commit()
