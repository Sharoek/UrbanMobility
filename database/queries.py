CREATE_USER_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL UNIQUE,
    role TEXT NOT NULL CHECK ( role IN ('service_engineer', 'system_admin'))
);
"""

CREATE_PROFILE_TABLE= """
CREATE TABLE IF NOT EXISTS profiles (
    id INTEGER PRIMARY  KEY AUTOINCREMEBT, 
    userid INTEGER NOT NULL UNIQUE,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL, 
    regdate TEXT NOT NULL,
    FOREIGN KEY (userid) REFERENCES users(id)
)
"""

INSERT_USER = "INSERT INTO users (username, password) VALUES (?, ?);"
GET_USER_BY_ID = "SELECT * FROM users WHERE id = ?;"
GET_ALL_USERS = "SELECT * FROM users;"
