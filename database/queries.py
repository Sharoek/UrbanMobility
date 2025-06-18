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


CREATE_SCOOTER_TABLE = """
CREATE TABLE IF NOT EXISTS scooters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand TEXT NOT NULL,
    model TEXT NOT NULL,
    serial_number TEXT NOT NULL UNIQUE CHECK (LENGTH(serial_number) BETWEEN 10 AND 17),
    top_speed REAL NOT NULL CHECK (top_speed > 0),
    battery_capacity REAL NOT NULL CHECK (battery_capacity > 0),
    state_of_charge REAL NOT NULL CHECK (state_of_charge >= 0 AND state_of_charge <= 100),
    min_soc REAL NOT NULL CHECK (min_soc >= 0 AND min_soc <= 100) ,
    max_soc REAL NOT NULL CHECK (max_soc >= 0 AND max_soc <= 100),
    latitude REAL CHECK (latitude BETWEEN 51.85 AND 51.99) CHECK (ABS(latitude * 100000 - CAST(latitude * 100000 AS INTEGER)) = 0),
    longitude REAL CHECK (longitude BETWEEN 4.36 AND 4.55) CHECK (ABS(longitude * 100000 - CAST(longitude * 100000 AS INTEGER)) = 0),
    out_of_service_status BOOLEAN NOT NULL DEFAULT 0,
    mileage REAL NOT NULL CHECK (mileage >= 0),
    last_maintenance_date TEXT NOT NULL CHECK (last_maintenance_date GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'),
    in_service_date TEXT NOT NULL DEFAULT (DATETIME('now'))
);
"""
CREATE_TRAVELLERS_TABLE = """
CREATE TABLE IF NOT EXISTS travellers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id TEXT NOT NULL UNIQUE, -- Could be a UUID or generated string
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    birthday TEXT NOT NULL CHECK (birthday GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'),
    gender TEXT NOT NULL CHECK (gender IN ('male', 'female')),
    street_name TEXT NOT NULL,
    house_number TEXT NOT NULL,
    zip_code TEXT NOT NULL CHECK (zip_code GLOB '[0-9][0-9][0-9][0-9][A-Z][A-Z]'),
    city TEXT NOT NULL CHECK (city IN (
        'Rotterdam', 'Amsterdam', 'Utrecht', 'The Hague', 'Eindhoven', 
        'Groningen', 'Leiden', 'Maastricht', 'Breda', 'Zwolle'
    )),
    email_address TEXT NOT NULL UNIQUE,
    mobile_phone TEXT NOT NULL CHECK (mobile_phone GLOB '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
    driving_license_number TEXT NOT NULL CHECK (
        driving_license_number GLOB '[A-Z][A-Z][0-9][0-9][0-9][0-9][0-9][0-9][0-9]' OR 
        driving_license_number GLOB '[A-Z][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'
    ),
    registration_date TEXT NOT NULL DEFAULT (DATETIME('now'))
);
"""

INSERT_USER = "INSERT INTO users (username, password, role, first_name, last_name, registration_date) VALUES (?, ?, ?, ?, ?, ?);"
GET_USER_BY_ID = "SELECT * FROM users WHERE id = ?;"
GET_ALL_USERS = "SELECT * FROM users;"
SEARCH_SCOOTER = "SELECT * FROM scooters WHERE brand LIKE ? OR id LIKE ? OR model LIKE ? OR serial_number LIKE ? OR top_speed LIKE ? OR battery_capacity LIKE ? OR state_of_charge LIKE ? OR min_soc LIKE ? OR max_soc LIKE ? OR latitude LIKE ? OR longitude LIKE ? OR mileage LIKE ?;"
# UPDATE_SCOOTER = "UPDATE scooters SET brand = ?, model = ?, serial_number = ?, top_speed = ?, battery_capacity = ?, state_of_charge = ?, min_soc = ?, max_soc = ?, max_soc = ?, latitude = ?, longitude = ?, out_of_service_status = ?, mileage = ?, last_maintenance_date = ? WHERE id = ?"
UPDATE_SCOOTER = "UPDATE scooters SET ? = ? WHERE id = ?"