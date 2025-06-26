from database.connection import get_connection
from models.user import User
from database.queries import INSERT_USER, GET_USER_BY_ID, GET_ALL_USERS
from encryption.encryption import encrypt_data
from encryption.hashing import verify_password, hash_password
import uuid

class seederRepository:
    def __init__(self):
        pass

    def save_scooter_to_db(self, scooter):
            """Save a scooter to the database."""
            #encrypt important information
            scooter.serial_number = encrypt_data(scooter.serial_number)
            scooter.latitude = encrypt_data(scooter.latitude)
            scooter.longitude = encrypt_data(scooter.longitude)
            
            with get_connection() as conn:
                try:
                    conn.execute(
                        "INSERT INTO scooters (brand, model, serial_number, top_speed, battery_capacity, state_of_charge, min_soc, max_soc, latitude, longitude, out_of_service_status, mileage, last_maintenance_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (scooter.brand, scooter.model, scooter.serial_number, scooter.top_speed, scooter.battery_capacity, scooter.state_of_charge, scooter.min_soc, scooter.max_soc, scooter.latitude, scooter.longitude, scooter.out_of_service_status, scooter.mileage, scooter.last_maintenance_date)
                    )
                    conn.commit()
                    print(f"[✔] Scooter '{scooter.serial_number}' added successfully.")
                except Exception as e:
                    print(f"[✖] Error saving scooter: {e}")
                    return False    

    def save_traveller_to_db(self, traveller):
        """Save a traveller to the database."""
        # Convert a UUID to a 32-character hexadecimal string
        customer_id = uuid.uuid4().hex
        traveller.first_name = encrypt_data(traveller.first_name)
        traveller.last_name = encrypt_data(traveller.last_name)
        traveller.birthday = encrypt_data(traveller.birthday)
        traveller.gender = encrypt_data(traveller.gender)
        traveller.street_name = encrypt_data(traveller.street_name)
        traveller.house_number = encrypt_data(traveller.house_number)
        traveller.zip_code = encrypt_data(traveller.zip_code)
        traveller.city = encrypt_data(traveller.city)
        traveller.email_address = encrypt_data(traveller.email_address)
        traveller.mobile_phone = encrypt_data(traveller.mobile_phone)
        traveller.driving_license_number = encrypt_data(traveller.driving_license_number)



        with get_connection() as conn:
            try:
                conn.execute(
                    "INSERT INTO travellers (customer_id, first_name, last_name, birthday, gender, street_name, house_number, zip_code, city, email_address, mobile_phone, driving_license_number) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (customer_id, traveller.first_name, traveller.last_name, traveller.birthday, traveller.gender, traveller.street_name, traveller.house_number, traveller.zip_code, traveller.city, traveller.email_address, traveller.mobile_phone, traveller.driving_license_number)
                )
                conn.commit()
                print(f"[✔] Traveller '{traveller.first_name} {traveller.last_name}' added successfully.")
            except Exception as e:
                print(f"[✖] Error saving traveller: {e}")
                return False