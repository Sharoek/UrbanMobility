from database.queries import SEARCH_TRAVELLER
from encryption.encryption import decrypt_data, encrypt_data
from encryption.hashing import hash_password
from database.connection import get_connection
from models.profile import Profile
from models.restorecode import restoreCode
from models.user import User

class adminRepository:
    def __init__(self):
        pass

    def view_users(self):
        try:
            with get_connection() as conn:
                cursor = conn.execute("SELECT username, role FROM users")
                rows = cursor.fetchall()
                if not rows:
                    print("[✖] No users found.")
                    return []
                print("[✔] Users:")
                for row in rows:
                    decrypted_username = decrypt_data(row[0])
                    print(f"Username: {decrypted_username}, Role: {row[1]}")
                return rows
        except Exception as e:
            print(f"[✖] Error viewing users: {e}")
            return []
    
    def get_users_by_role(self, role):
        try:
            with get_connection() as conn:
                cursor = conn.execute("SELECT * FROM users WHERE role = ?", (role,))
                rows = cursor.fetchall()
                if not rows:
                    print(f"[✖] No users found with role '{role}'.")
                    return []
                print(f"[✔] Users with role '{role}':")
                #return a list models
                users = []
                for row in rows:
                    decrypted_username = decrypt_data(row[1])
                    decrypted_firstname = decrypt_data(row[4])
                    decrypted_lastname = decrypt_data(row[5])
                    
                    user = row[0], decrypted_username, row[2], row[3], decrypted_firstname, decrypted_lastname, row[6]
                    users.append(user)
                return users
        except Exception as e:
            print(f"[✖] Error getting users: {e}")
            return []
        
    def get_user_by_id(self, user_id):
        try:
            with get_connection() as conn:
                cursor = conn.execute("SELECT * FROM users WHERE id = ?", (user_id, ))
                row = cursor.fetchone()
                if not row:
                    print(f"[✖] No user found with ID '{user_id}'.")
                    return None
                decrypted_username = decrypt_data(row[1])
                decrypted_firstname = decrypt_data(row[4])
                decrypted_lastname = decrypt_data(row[5])

                user = row[0], decrypted_username, row[2], row[3], decrypted_firstname, decrypted_lastname, row[6]
                return user
        except Exception as e:
            print(f"[✖] Error getting user: {e}")
            return None
        
    def update_user(self, user_id: int, item: str, value):
        """Update a specific field of a user in the database."""
        allowed_columns = {
            "username",
            "password",  # should be hashed before passing
            "role",
            "first_name",
            "last_name",
        }

        if item not in allowed_columns:
            print(f"[✖] Invalid field: '{item}' is not allowed to be updated.")
            return False

        if item == "password":
            from encryption.hashing import hash_password
            value = hash_password(value)
        
        if item == "username" or item == "first_name" or item == "last_name":
            value = encrypt_data(value)
            

        query = f"UPDATE users SET {item} = ? WHERE id = ?"
        try:
            with get_connection() as conn:
                conn.execute(query, (value, user_id))
                conn.commit()
                print(f"[✔] User ID {user_id}: '{item}' updated successfully.")
                return True
        except Exception as e:
            print(f"[✖] Error updating user: {e}")
            return False
        
    def delete_user(self, user_id: int, acting_role: str = ""):
        """Delete a user from the database, based on acting user's role."""
        if not acting_role:
            print("[✖] Role is required to delete a user.")
            return False

        # Define role-based deletion rules
        if acting_role == "system_admin":
            allowed_roles = ["service_engineer"]
        elif acting_role == "super_admin":
            allowed_roles = ["service_engineer", "system_admin"]
        else:
            print("[✖] Unauthorized role.")
            return False

        try:
            with get_connection() as conn:
                # Get the role of the user we want to delete
                cursor = conn.execute("SELECT role FROM users WHERE id = ?", (user_id,))
                row = cursor.fetchone()

                if not row:
                    print(f"[✖] User ID {user_id} does not exist.")
                    return False

                target_role = row[0]

                # Check if deletion is allowed
                if target_role not in allowed_roles:
                    print(f"[✖] You are not allowed to delete a user with the role '{target_role}'.")
                    return False

                # Proceed with deletion
                conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
                conn.commit()
                print(f"[✔] User ID {user_id} ({target_role}) deleted successfully.")
                return True

        except Exception as e:
            print(f"[✖] Error deleting user: {e}")
            return False

    def reset_password(self, user_id, new_password):
        """Reset the password of a user."""
        hashed_password = hash_password(new_password)
        query = "UPDATE users SET password = ? WHERE id = ?"
        try:
            with get_connection() as conn:
                conn.execute(query, (hashed_password, user_id))
                conn.commit()
                print(f"[✔] Password updated successfully for user ID {user_id}.")
                return True
        except Exception as e:
            print(f"[✖] Error updating password: {e}")
            return False
    
    def getUserID(self, username):
        username = encrypt_data(username)
        try:
            with get_connection() as conn:
                cursor = conn.execute("SELECT id FROM users WHERE username = ?", (username,))
                row = cursor.fetchone()
                if not row:
                    print(f"[✖] No user found with username '{username}'.")
                    return None
                return row[0]
        except Exception as e:
            print(f"[✖] Error getting user ID: {e}")
            return None
    
    def delete_own_account(self, user_id):
        try:
            with get_connection() as conn:
                conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
                conn.commit()
                print(f"[✔] User ID {user_id} deleted successfully.")
                return True
        except Exception as e:
            print(f"[✖] Error deleting user: {e}")
            return False
        
    def get_all_travellers(self):
        try:
            with get_connection() as conn:
                cursor = conn.execute("SELECT * FROM travellers")
                rows = cursor.fetchall()
                if not rows:
                    print("[✖] No travellers found.")
                    return []
                return rows
        except Exception as e:
            print(f"[✖] Error getting travellers: {e}")
            return []
    
    def decrypt_travellers(self, travellers):
        decrypted_travellers = []
        for traveller in travellers:
            decrypted_traveller = dict(traveller)
            decrypted_traveller['first_name'] = decrypt_data(traveller['first_name'])
            decrypted_traveller['last_name'] = decrypt_data(traveller['last_name'])
            decrypted_traveller['birthday'] = decrypt_data(traveller['birthday'])
            decrypted_traveller['gender'] = decrypt_data(traveller['gender'])
            decrypted_traveller['street_name'] = decrypt_data(traveller['street_name'])
            decrypted_traveller['house_number'] = decrypt_data(traveller['house_number'])
            decrypted_traveller['zip_code'] = decrypt_data(traveller['zip_code'])
            decrypted_traveller['city'] = decrypt_data(traveller['city'])
            decrypted_traveller['email_address'] = decrypt_data(traveller['email_address'])
            decrypted_traveller['mobile_phone'] = decrypt_data(traveller['mobile_phone'])
            decrypted_traveller['driving_license_number'] = decrypt_data(traveller['driving_license_number'])
            decrypted_travellers.append(decrypted_traveller)
        return decrypted_travellers
    

    def search_traveller(self, search_key: str, detailed: bool = False):
        search_key_lower = search_key.lower()

        travellers = self.get_all_travellers()              # fetch all (encrypted) rows
        decrypted_travellers = self.decrypt_travellers(travellers)  # decrypt encrypted fields

        matched_travellers = []

        for row in decrypted_travellers:
            # Fields to search in, all decrypted/ready-to-compare
            fields_to_check = [
                "customer_id",
                "first_name",
                "last_name",
                "birthday",
                "gender",
                "street_name",
                "house_number",
                "zip_code",
                "city",
                "email_address",
                "mobile_phone",
                "driving_license_number",
                "registration_date"
            ]

            matched_fields = []
            for field in fields_to_check:
                value = str(row.get(field, "")).lower()
                if search_key_lower in value:
                    matched_fields.append(field)

            if matched_fields:
                matched_travellers.append((row, matched_fields))

        if not matched_travellers:
            print(f"[✖] No travellers found matching '{search_key}'.")
            return []

        if not detailed:
            print(f"[✔] Found {len(matched_travellers)} traveller(s) matching '{search_key}':")

            for row, matched_fields in matched_travellers:
                matched_fields_str = ", ".join(matched_fields) if matched_fields else "no specific field?"
                print(f"  - ID: {row['id']}, Name: {row['first_name']} {row['last_name']}  [Matched on: {matched_fields_str}]")

        return [row for row, _ in matched_travellers]


    def delete_scooter(self, scooter_id):
        try:
            with get_connection() as conn:
                conn.execute("DELETE FROM scooters WHERE id = ?", (scooter_id,))
                conn.commit()
                print(f"[✔] Scooter ID {scooter_id} deleted successfully.")
                return True
        except Exception as e:
            print(f"[✖] Error deleting scooter: {e}")
            return False

    def update_traveller(self, customer_id, item, value):
        """Update a specific field of a traveller in the database."""
        allowed_columns = {
            "first_name",
            "last_name",
            "gender",
            "street_name",
            "house_number",
            "zip_code",
            "city",
            "email_address",
            "mobile_phone",
            "driving_license_number",
        }

        if item not in allowed_columns:
            print(f"[✖] Invalid field: '{item}' is not allowed to be updated.")
            return False

      
        value = encrypt_data(value)

        query = f"UPDATE travellers SET {item} = ? WHERE customer_id = ?"
        try:
            with get_connection() as conn:
                conn.execute(query, (value, customer_id))
                conn.commit()
                print(f"[✔] Traveller ID {customer_id}: '{item}' updated successfully.")
                return True
        except Exception as e:
            print(f"[✖] Error updating traveller: {e}")
            return False
        
    def delete_traveller(self, customer_id):
        try:
            with get_connection() as conn:
                conn.execute("DELETE FROM travellers WHERE customer_id = ?", (customer_id, ))
                conn.commit()
                print(f"[✔] Traveller ID {customer_id} deleted successfully.")
                return True
        except Exception as e:
            print(f"[✖] Error deleting traveller: {e}")
            return False
        
    def add_restorecode(self, restorecode: restoreCode):
        if not restorecode:
            print("[✖] Restore code is required.")
            return False
        #encode necessary 
        restorecode.code = encrypt_data(restorecode.code)
        restorecode.backup_filename = encrypt_data(restorecode.backup_filename)

        try:
            with get_connection() as conn:
                conn.execute(
                    "INSERT INTO restore_codes (code, user_id, backup_filename, used, generated_at) VALUES (?, ?, ?, ?, ?)",
                    (restorecode.code, restorecode.user_id, restorecode.backup_filename, restorecode.used, restorecode.generated_at),
                )
                conn.commit()
                print(f"[✔] Restore code added successfully.")
                return True
        except Exception as e:
            print(f"[✖] Error adding restore code: {e}")
            return False
        
    def update_restorecode_used(self, used: bool, id: int):       
        try:
            with get_connection() as conn:
                conn.execute(
                    "UPDATE restore_codes SET used = ? WHERE id = ?",
                    (used, id),
                )
                conn.commit()
                print(f"[✔] Restore code column used updated successfully.")
                return True
        except Exception as e:
            print(f"[✖] Error updating restore code: {e}")
            return False
        
    def get_all_restorecodes_used_is_true(self):
        try:
            with get_connection() as conn:
                cursor = conn.execute("SELECT * FROM restore_codes WHERE used = 1") 
                rows = cursor.fetchall()
                if not rows:
                    print("[✖] No restore codes found.")
                    return []
                return rows
        except Exception as e:
            print(f"[✖] Error getting restore codes: {e}")
            return []
    
    def decrypt_restorecodes(self, restore_codes):
        decrypted_restore_codes = []
        for restore_code in restore_codes:
            decrypted_restore_code = dict(restore_code)
            decrypted_restore_code['code'] = decrypt_data(restore_code['code'])
            decrypted_restore_code['backup_filename'] = decrypt_data(restore_code['backup_filename'])
            decrypted_restore_code['used'] = restore_code['used']
            decrypted_restore_codes.append(decrypted_restore_code)
        return decrypted_restore_codes
    
    def get_restorecodes_by_user(self, user_name):
        user_name = encrypt_data(user_name)
        try:
            with get_connection() as conn:
                cursor = conn.execute("SELECT * FROM restore_codes WHERE user_id = (SELECT id FROM users WHERE username = ?)", (user_name,))
                rows = cursor.fetchall()
                if not rows:
                    print("[✖] No restore codes found.")
                    return []
                return rows
        except Exception as e:
            print(f"[✖] Error getting restore codes: {e}")
            return []
    
    def load_restore_code(self):
        try:
            with get_connection() as conn:
                cursor = conn.execute("SELECT * FROM restore_codes")
                rows = cursor.fetchall()
                if not rows:
                    print("[✖] No restore codes found.")
                    return []
                restore_codes = [
               restoreCode(
                    id=row["id"],
                    code=row["code"],
                    backup_filename=row["backup_filename"],
                    used=row["used"],
                    user_id=row["user_id"],
                    generated_at=row["generated_at"]
                ) for row in rows
            ]
            return restore_codes
        except Exception as e:
            print(f"[✖] Error getting restore codes: {e}")
            return []
    
    def re_insertcodes(self, restore_codes: list[restoreCode]):
        try:
            with get_connection() as conn:
                for restore_code in restore_codes:
                    print(f"Insert id={restore_code.id} code={restore_code.code} user_id={restore_code.user_id}")
                    conn.execute(
                        "INSERT INTO restore_codes (id, code, user_id, backup_filename, used, generated_at) VALUES (?, ?, ?, ?, ?, ?)",
                        (
                            restore_code.id,
                            restore_code.code,
                            restore_code.user_id,
                            restore_code.backup_filename,
                            restore_code.used,
                            restore_code.generated_at
                        ),
                    )
                conn.commit()
                print(f"[✔] Restore codes re-inserted successfully.")
                return True
        except Exception as e:
            print(f"[✖] Error re-inserting restore codes: {e}")
            return False

