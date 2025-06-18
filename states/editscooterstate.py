from states.appstate import AppState
from encryption.validators import verify_number_input, validate_and_normalize_coord, check_mileage, validate_last_maintanence
from models.scooter import Scooter

class editScooterState(AppState):
    def __init__(self, context):
        self.context = context

    def run(self):
        self.display_scooter_list()   
        self.context.go_back()  # Go back to the previous state after editing


    def display_scooter_list(self):
        print("Displaying scooters:")
        count = 1
        scooters = self.context.user_repo.get_scooters()
        for scooter in scooters:
            print(f"{count}. ID: {scooter.id}, Model: {scooter.model}, Brand: {scooter.brand}")
            count += 1
        print("\nSelect an option:")
        choice = verify_number_input("Enter your choice:", 1, len(scooters))    
        try:
            selected_scooter = scooters[choice - 1]
            print(f"You selected: {selected_scooter.model} ({selected_scooter.brand})")
            self.show_sub_menu(selected_scooter)
            return 
        except IndexError:
            print("Invalid choice. Please try again.")
            return self.display_scooter_list()


    def show_sub_menu(self, selected_scooter: Scooter):
        print("Sub-menu for editing scooter details:")
        self.display_scooter_details(selected_scooter)
        print("1. State of Charge")
        print("2. Tartget range SoC (min/max)")
        print("3. Location (latitude/longitude)")
        print("4. Out of Service Status")
        print("5. Mileage")
        print("6. Last Maintenance Date")
        print("0. Go Back")
        choice = verify_number_input("Enter your choice: ", 0, 6)

        if choice == 1:
            self.soc(selected_scooter)
        if choice == 2:
            self.sub_menu_soc(selected_scooter)
        if choice == 3:
            self.sub_menu_location(selected_scooter)
        if choice == 4:
            self.out_of_service_status(selected_scooter)
        if choice == 5:
            self.sub_menu_mileage(selected_scooter)
        if choice == 6:
            self.sub_menu_last_maintenance(selected_scooter)
        if choice == 0:
            self.context.go_back()
        else:
            self.show_sub_menu(selected_scooter)


    def soc(self, selected_scooter: Scooter):
        new_soc = verify_number_input("Enter new State of Charge (0-100): ", 0, 100)
        selected_scooter.state_of_charge = new_soc
        try:
            self.context.user_repo.edit_scooter(selected_scooter, "state_of_charge", new_soc)
            print(f"State of Charge updated to {new_soc}%")
        except Exception as e:
            print(f"[✖] Error updating State of Charge: {e}")
        self.show_sub_menu(selected_scooter)


    def sub_menu_last_maintenance(self, selected_scooter: Scooter):
        print(f"Current Last Maintenance Date: {selected_scooter.last_maintenance_date}")
        new_date = input("Enter new Last Maintenance Date (YYYY-MM-DD): ")
        prev_date = selected_scooter.last_maintenance_date
        try:
            if validate_last_maintanence(new_date, prev_date):
                selected_scooter.last_maintenance_date = new_date
                self.context.user_repo.edit_scooter(selected_scooter, "last_maintenance_date", new_date)
                print(f"Last Maintenance Date updated to {new_date}")
        except Exception as e:
            print(f"[✖] Error updating Last Maintenance Date: {e}")
        self.show_sub_menu(selected_scooter)



    def sub_menu_mileage(self, selected_scooter: Scooter):
        print(f"Current Mileage: {selected_scooter.mileage} km")
        new_mileage = verify_number_input("Enter new Mileage (km): ", 0, 20000, float)
        if check_mileage(new_mileage, selected_scooter.mileage):
            selected_scooter.mileage = new_mileage
        try:
            self.context.user_repo.edit_scooter(selected_scooter, "mileage", new_mileage)
            print(f"Mileage updated to {new_mileage} km")
        except Exception as e:
            print(f"[✖] Error updating Mileage: {e}")
        self.show_sub_menu(selected_scooter)        



    def sub_menu_soc(self, selected_scooter: Scooter):
        print(f"Minimum Soc: {selected_scooter.min_soc}% | Maximum SoC: {selected_scooter.max_soc}%")
        print("1. Minimum SoC")
        print("2. Maximum SoC")
        print("0. Go Back")
        choice = verify_number_input("Enter your choice: ", 0, 2)
        if choice == 1:
            new_min_soc = verify_number_input("Enter new Minimum SoC (0-100): ", 0, 100)
            selected_scooter.min_soc = new_min_soc
            try:
                self.context.user_repo.edit_scooter(selected_scooter, "min_soc", new_min_soc)
                print(f"Minimum SoC updated to {new_min_soc}%")
            except Exception as e:
                print(f"[✖] Error updating Minimum SoC: {e}")
        elif choice == 2:
            new_max_soc = verify_number_input("Enter new Maximum SoC (0-100): ", 0, 100)
            selected_scooter.max_soc = new_max_soc
            try:
                self.context.user_repo.edit_scooter(selected_scooter, "max_soc", new_max_soc)
                print(f"Maximum SoC updated to {new_max_soc}%")
            except Exception as e:
                print(f"[✖] Error updating Maximum SoC: {e}")
        else:
            print("Invalid choice. Please try again.")
        if choice == 0:
            self.show_sub_menu(selected_scooter)

    def sub_menu_location(self, selected_scooter: Scooter):
        print(f"Current Location: Latitude {selected_scooter.latitude}, Longitude {selected_scooter.longitude}")
        print("1. Update Latitude")
        print("2. Update Longitude")
        print("0. Go Back")
        choice = verify_number_input("Enter your choice: ", 0, 2)
        if choice == 1:
            new_latitude = verify_number_input("Enter new Latitude (51.85000 to 51.99000): ", 51.85000, 51.99000, float)
            new_latitude = validate_and_normalize_coord(new_latitude, 5)
            selected_scooter.latitude = new_latitude
            try:
                self.context.user_repo.edit_scooter(selected_scooter, "latitude", new_latitude)
                print(f"Latitude updated to {new_latitude}")
            except Exception as e:
                print(f"[✖] Error updating Latitude: {e}")
        elif choice == 2:
            new_longitude = verify_number_input("Enter new Longitude (4.36000 to 4.55000): ", 4.36000, 4.55000, float)
            new_longitude = validate_and_normalize_coord(new_longitude, 5)
            selected_scooter.longitude = new_longitude
            try:
                self.context.user_repo.edit_scooter(selected_scooter, "longitude", new_longitude)
                print(f"Longitude updated to {new_longitude}")
            except Exception as e:
                print(f"[✖] Error updating Longitude: {e}")
        else:
            print("Invalid choice. Please try again.")
        if choice == 0:
            self.show_sub_menu(selected_scooter)
            
    def out_of_service_status(self, selected_scooter: Scooter):
        print(f"Current Out of Service Status: {'Yes' if selected_scooter.out_of_service_status else 'No'}")
        print("1. Set Out of Service")
        print("2. Set In Service")
        print("0. Go Back")
        choice = verify_number_input("Enter your choice: ", 0, 2)
        if choice == 1:
            selected_scooter.out_of_service_status = True
            try:
                self.context.user_repo.edit_scooter(selected_scooter, "out_of_service_status", True)
                print("Scooter set to Out of Service.")
            except Exception as e:
                print(f"[✖] Error setting Out of Service: {e}")
        elif choice == 2:
            selected_scooter.out_of_service_status = False
            try:
                self.context.user_repo.edit_scooter(selected_scooter, "out_of_service_status", False)
                print("Scooter set to In Service.")
            except Exception as e:
                print(f"[✖] Error setting In Service: {e}")
        elif choice == 0:
            self.show_sub_menu(selected_scooter)
        else:
            print("Invalid choice. Please try again.")


    def display_scooter_details(self, scooter: Scooter):
        print(f"ID: {scooter.id}")
        print(f"Model: {scooter.model}")
        print(f"Brand: {scooter.brand}")
        print(f"Serial Number: {scooter.serial_number}")
        print(f"Top Speed: {scooter.top_speed} km/h")
        print(f"Battery Capacity: {scooter.battery_capacity} Wh")
        print(f"State of Charge: {scooter.state_of_charge}%")
        print(f"Minimum SOC: {scooter.min_soc}%")
        print(f"Maximum SOC: {scooter.max_soc}%")
        print(f"Latitude: {scooter.latitude}")
        print(f"Longitude: {scooter.longitude}")
        print(f"Out of Service Status: {'Yes' if scooter.out_of_service_status else 'No'}")
        print(f"Mileage: {scooter.mileage} km")
        print(f"Last Maintenance Date: {scooter.last_maintenance_date}")