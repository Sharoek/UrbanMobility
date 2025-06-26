import os
from database import init_db
from pathlib import Path
from database import seeder
from states.appcontext import AppContext


if __name__ == "__main__":
    from database import init_db, seeder
    import os
    from pathlib import Path

    if not os.path.exists(Path("UM.db")):
        print("[i] Initializing database...")
        init_db.initialize_database()
        seeder.seed_database()
    else:
        print("[i] Database found.")

    app = AppContext()
    app.run()