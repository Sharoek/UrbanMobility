CREATE_USER_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL UNIQUE,
    role TEXT NOT NULL CHECK ( role IN ('service_engineer', 'system_admin')),
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    registration_date TEXT NOT NULL
);
"""

INSERT_USER = "INSERT INTO users (username, password, role, first_name, last_name, registration_date) VALUES (?, ?, ?, ?, ?, ?);"
GET_USER_BY_ID = "SELECT * FROM users WHERE id = ?;"
GET_ALL_USERS = "SELECT * FROM users;"

