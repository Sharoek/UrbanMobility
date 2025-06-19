from database.connection import get_connection
from models.scooter import Scooter
from models.user import User
from database.queries import INSERT_USER, GET_USER_BY_ID, GET_ALL_USERS, SEARCH_SCOOTER, UPDATE_SCOOTER
from encryption.encryption import encrypt_data
from encryption.hashing import verify_password, hash_password

class UserRepository:
    def __init__(self):
        pass    

    def save_user_to_db(self, user: User):
        with get_connection() as conn:
            encrypted_first = encrypt_data(user.profile.first_name)
            encrypted_last = encrypt_data(user.profile.last_name)
            encrypt_username = encrypt_data(user.username)
            try:
                conn.execute(INSERT_USER, (encrypt_username, user.password_hash, user.role, encrypted_first, encrypted_last, user.profile.registration_date))
                conn.commit()
                print(f"[✔] User '{user.username}' added as {user.role}.")
            except Exception as e:
                print(f"[✖] Error saving user: {e}")
                return False
    
    def authenticate_user(self, username: str, password: str) -> bool:
        """Authenticate user by checking username and password."""
        # hash password is not the same as in the database so get password hash from the database and decrypt it
        username = encrypt_data(username)
        print(f"[i] Authenticating user: {username}")
        with get_connection() as conn:
            cursor = conn.execute("SELECT password FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            if verify_password(password, row["password"]):
                print("[✔] Authentication successful.")
                return True
        return False
    
    def get_user_role(self, username: str) -> str:
        """Get the role of a user by username."""
        username = encrypt_data(username)
        with get_connection() as conn:
            cursor = conn.execute("SELECT role FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            if row:
                return row["role"]
        return "unknown"
    
    def update_password(self, username: str, new_password: str) -> bool:
        """Update the password for a user."""
        username = encrypt_data(username)
        new_password_hash = hash_password(new_password)
        with get_connection() as conn:
            try:
                conn.execute("UPDATE users SET password = ? WHERE username = ?", (new_password_hash, username))
                conn.commit()
                print(f"[✔] Password for user '{username}' has been updated successfully.")
                return True
            except Exception as e:
                print(f"[✖] Error updating password: {e}")
                return False
    #redundant?
    def update_own_password(self, username: str, old_password: str, new_password: str) -> bool:
        """Update the password for the currently logged-in user."""
        if not self.authenticate_user(username, old_password):
            print("[✖] Old password is incorrect.")
            return False
        return self.update_password(username, new_password)
    
    def search_scooter(self, search_key: str, detailed: bool = False):
        search_key_lower = search_key.lower()

        with get_connection() as conn:
            cursor = conn.execute(
                SEARCH_SCOOTER,
                tuple(f"%{search_key}%" for _ in range(12))
            )
            rows = cursor.fetchall()

            if not rows:
                print(f"[✖] No scooters found matching '{search_key}'.")
                return []

            if not detailed:
                print(f"[✔] Found {len(rows)} scooter(s) matching '{search_key}':")

                for row in rows:
                    # List of fields to check for match
                    fields_to_check = [
                        "model",
                        "brand",
                        "serial_number",
                        "top_speed",
                        "battery_capacity",
                        "state_of_charge",
                        "min_soc",
                        "max_soc",
                        "latitude",
                        "longitude",
                        "out_of_service_status",
                        "mileage",
                        # You can add last_maintenance_date too if you want
                    ]

                    matched_fields = []
                    for field in fields_to_check:
                        # Convert field to string and lower-case for comparison
                        value = str(row[field]).lower()
                        if search_key_lower in value:
                            matched_fields.append(field)

                    matched_fields_str = ", ".join(matched_fields) if matched_fields else "no specific field?"

                    print(f"  - ID: {row['id']}, Model: {row['model']}, Brand: {row['brand']}  [Matched on: {matched_fields_str}]")

                return []

            # If detailed=True, return full scooter objects (no print)
            return [
                Scooter(
                    id=row["id"],
                    model=row["model"],
                    brand=row["brand"],
                    serial_number=row["serial_number"],
                    top_speed=row["top_speed"],
                    battery_capacity=row["battery_capacity"],
                    state_of_charge=row["state_of_charge"],
                    min_soc=row["min_soc"],
                    max_soc=row["max_soc"],
                    latitude=row["latitude"],
                    longitude=row["longitude"],
                    out_of_service_status=row["out_of_service_status"],
                    mileage=row["mileage"],
                    last_maintenance_date=row["last_maintenance_date"],
                )
                for row in rows
            ]

        
    def edit_scooter(self, scooter: Scooter, item, value):
        """Edit scooter details in the database."""
        allowed_columns = {
            "model": scooter.model,
            "brand": scooter.brand,
            "serial_number": scooter.serial_number,
            "top_speed": scooter.top_speed,
            "battery_capacity": scooter.battery_capacity,
            "state_of_charge": scooter.state_of_charge,
            "min_soc": scooter.min_soc,
            "max_soc": scooter.max_soc,
            "latitude": scooter.latitude,
            "longitude": scooter.longitude,
            "out_of_service_status": scooter.out_of_service_status,
            "mileage": scooter.mileage,
            "last_maintenance_date": scooter.last_maintenance_date,
        }
        if item not in allowed_columns:
            print(f"[✖] Invalid column name: {item}")
            return False
        if item == "longitude" or item == "latitude":
            # if the value has less than 5 decimal places, it will be rounded to 5 decimal places
            # check how many decimal places the value has
            # if the value has more than 5 decimal places, it will be rounded to 5 decimal places
            # if the value has less than 5 decimal places, it will be rounded to 5 decimal places
            if len(str(value).split(".")[1]) < 5:
                value = f"{value:.5f}"
            if len(str(value).split(".")[1]) > 5:
                value = f"{value:.5f}"

            
        query = f"UPDATE scooters SET {item} = ? WHERE id = ?"
        with get_connection() as conn:
            try:
                conn.execute(
                    query,
                    (
                        value,  # The new value for the specified item
                        scooter.id  # The ID of the scooter to update
                    )
                )
                conn.commit()
                print(f"[✔] Scooter '{scooter.serial_number}' details updated successfully.")
            except Exception as e:
                print(f"[✖] Error updating scooter: {e}")
                return False
            
    def get_scooters(self):
        """Retrieve all scooters from the database."""
        with get_connection() as conn:
            cursor = conn.execute("SELECT * FROM scooters")
            rows = cursor.fetchall()
            if not rows:
                print("[✖] No scooters found in the database.")
                return []
            
            return [
                Scooter(
                    id=row["id"],
                    model=row["model"],
                    brand=row["brand"],
                    serial_number=row["serial_number"],
                    top_speed=row["top_speed"],
                    battery_capacity=row["battery_capacity"],
                    state_of_charge=row["state_of_charge"],
                    min_soc=row["min_soc"],
                    max_soc=row["max_soc"],
                    latitude=row["latitude"],
                    longitude=row["longitude"],
                    out_of_service_status=row["out_of_service_status"],
                    mileage=row["mileage"],
                    last_maintenance_date=row["last_maintenance_date"]
                )
                for row in rows
            ]