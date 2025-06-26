from datetime import  datetime
from states.appstate import AppState
from encryption.validators import get_valid_input, validate_and_normalize_coord, validate_brand, validate_model, validate_serial_number, verify_number_input
from log.manager import LogManager
from database.seederRepository import seederRepository
from models.scooter import Scooter

class addScooterState(AppState):
    def __init__(self, context):
        super().__init__(context)
        self.log_manager = LogManager()
        self.seeder_repository = seederRepository()
        
    def run(self):
        try:
            scooter = self.create_scooter_details()
            self.seeder_repository.save_scooter_to_db(scooter)
            print(f"[✔] Scooter '{scooter.brand} {scooter.model}' added successfully.")
            self.log_manager.log(self.context.username, "added scooter", f"Added scooter: {scooter.brand}", False)
        except Exception as e:
            print(f"[✖] {e}")
            self.log_manager.log(self.context.username, "failed to add scooter", "", True)
        finally:
            self.context.go_back()

    def create_scooter_details(self):
        try:
            brand = get_valid_input("Enter scooter brand: ", validate_brand, "Invalid brand", username=self.context.username)
            model = get_valid_input("Enter scooter model: ", validate_model, "Invalid model", username=self.context.username)
            serial_number = get_valid_input("Enter serial number: ", validate_serial_number, "Invalid serial number", username=self.context.username)
            top_speed = verify_number_input("Enter top speed: ", 15, 80)
            battery_capacity = verify_number_input("Enter battery capacity: ", 200, 1000)
            state_of_charge = verify_number_input("Enter State of Charge (0-100): ", 0, 100)
            min_soc = verify_number_input("Enter Minimum SoC (0-100): ", 0, 100)
            max_soc = verify_number_input("Enter Maximum SoC (0-100): ", 0, 100)
            if max_soc < min_soc:
                self.log_manager.log(self.context.username, "failed to add scooter", "", True)
                raise Exception("Maximum SoC cannot be less than Minimum SoC")
            latitude = verify_number_input("Enter Latitude (51.85000 to 51.99000): ", 51.85000, 51.99000, float)
            normalised_latitude = validate_and_normalize_coord(latitude, 5)
            longitude = verify_number_input("Enter Longitude (4.36000 to 4.55000): ", 4.36000, 4.55000, float)
            normalised_longitude = validate_and_normalize_coord(longitude, 5)
            out_of_service_status = verify_number_input("Is the scooter out of service?\n Enter 0 for yes or 1 for no: ", 0, 1)
            if out_of_service_status == 1:
                out_of_service_status = False
            elif out_of_service_status == 0:
                out_of_service_status = True
            mileage = verify_number_input("Enter new Mileage (km): ", 0, 20000, float)
            last_maintenance_date = datetime.now().strftime("%Y-%m-%d")
            scooter = Scooter(
                brand=brand,
                model=model,
                serial_number=serial_number,
                top_speed=top_speed,
                battery_capacity=battery_capacity,
                state_of_charge=state_of_charge,
                min_soc=min_soc,
                max_soc=max_soc,
                latitude=normalised_latitude,
                longitude=normalised_longitude,
                out_of_service_status=out_of_service_status,
                mileage=mileage,
                last_maintenance_date=last_maintenance_date
            )
            return scooter
        except Exception as e:
            raise Exception(f"Error collecting scooter details: {e}")

