import os
from database import init_db
from pathlib import Path

def setup():
    # Check if database exists, if not, initialize
    if not os.path.exists(Path("UM.db")):
        print("[i] Initializing database...")
        init_db.initialize_database()
        
    else:
        print("[i] Database found.")



if __name__ == "__main__":
    setup()