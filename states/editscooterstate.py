from models.scooter import Scooter
from states.appstate import AppState
from encryption.validators import check_mileage, validate_and_normalize_coord, validate_brand, validate_last_maintanence, validate_model, validate_serial_number, verify_number_input

class editScooterState(AppState):
    def run(self):
        self.display_scooter_list()   
        self.context.set_state(editScooterState(self.context))

    def display_scooter_list(self):
        print("Displaying scooters:")
        count = 1
        scooters = self.context.user_repo.get_scooters()
        for scooter in scooters:
            print(f"{count}. ID: {scooter.id}, Model: {scooter.model}, Brand: {scooter.brand}")
            count += 1    
        print("0. Go Back")    
        print("\nSelect an option:")
        choice = verify_number_input("Enter your choice:", 0, len(scooters))   
        if choice == 0:
            return self.context.go_back() 
        try:
            selected_scooter = scooters[choice - 1]
            print(f"You selected: {selected_scooter.model} ({selected_scooter.brand})")
            self.scooter_submenu(selected_scooter)
        except IndexError:
            print("Invalid choice. Please try again.")
            return self.display_scooter_list()
    
    def scooter_submenu(self, selected_scooter):
        print("Scooter Sub Menu")
        try:
            if self.context.role == "system_admin" or self.context.role == "super_admin":
                self.show_admin_sub_menu(selected_scooter)
            if self.context.role == "service_engineer":
                self.show_sub_menu(selected_scooter)
        except Exception as e:
            print(f"[✖] Error: {e}")
    
    def show_admin_sub_menu(self, selected_scooter: Scooter):
        print("Sub-menu for editing scooter details:")
        self.display_scooter_details(selected_scooter)
        print("1. Brand")
        print("2. Model")
        print("3. Serial Number")
        print("4. Top speed")
        print("5. Battery capacity")
        print("6. State of Charge")
        print("7. Tartget range SoC (min/max)")
        print("8. Location (latitude/longitude)")
        print("9. Out of Service Status")
        print("10. Mileage")
        print("11. Last Maintenance Date")
        print("0. Go Back")

        choice = verify_number_input("Enter your choice: ", 0, 11)
        if choice == 1:
            self.edit_brand(selected_scooter)
        if choice == 2:
            self.edit_model(selected_scooter)
        if choice == 3:
            self.edit_serial_number(selected_scooter)
        if choice == 4:
            self.edit_top_speed(selected_scooter)
        if choice == 5:
            self.edit_battery_capacity(selected_scooter)    
        if choice == 6:
            self.soc(selected_scooter)
        if choice == 7:
            self.sub_menu_soc(selected_scooter)
        if choice == 8:
            self.sub_menu_location(selected_scooter)
        if choice == 9:
            self.out_of_service_status(selected_scooter)
        if choice == 10:
            self.sub_menu_mileage(selected_scooter)
        if choice == 11:
            self.sub_menu_last_maintenance(selected_scooter)
        if choice == 0:
            self.context.go_back()
        else:
            self.show_admin_sub_menu(selected_scooter)

    def edit_model(self, selected_scooter: Scooter):
        if self.context.role != "system_admin" and self.context.role != "super_admin":
            print("You do not have permission to edit model.")
            return

        new_model = input("Enter new model: ")
        if validate_model(new_model):
            selected_scooter.model = new_model
            try:
                self.context.user_repo.edit_scooter(selected_scooter, "model", new_model)
                print(f"Model updated to {new_model}")
            except Exception as e:
                print(f"[✖] Error updating model: {e}")
        else:
            print("Invalid format of model")

    def edit_serial_number(self, selected_scooter: Scooter):
        if self.context.role != "system_admin" and self.context.role != "super_admin":
            print("You do not have permission to edit serial number.")
            return

        new_serial_number = input("Enter new serial number: ")
        if validate_serial_number(new_serial_number):
            selected_scooter.serial_number = new_serial_number
            try:
                self.context.user_repo.edit_scooter(selected_scooter, "serial_number", new_serial_number)
                print(f"Serial number updated to {new_serial_number}")
            except Exception as e:
                print(f"[✖] Error updating serial number: {e}")
        else: 
            print("Invalid format of serial number")

    def edit_top_speed(self, selected_scooter: Scooter):
        if self.context.role != "system_admin" and self.context.role != "super_admin":
            print("You do not have permission to edit top speed.")
            return

        new_top_speed = verify_number_input("Enter new top speed: ", 15, 80)
        selected_scooter.top_speed = new_top_speed
        try:
            self.context.user_repo.edit_scooter(selected_scooter, "top_speed", new_top_speed)
            print(f"Top speed updated to {new_top_speed}")
        except Exception as e:
            print(f"[✖] Error updating top speed: {e}")

    def edit_battery_capacity(self, selected_scooter: Scooter):
        if self.context.role != "system_admin" and self.context.role != "super_admin":
            print("You do not have permission to edit battery capacity.")
            return

        new_battery_capacity = verify_number_input("Enter new battery capacity: ", 200, 1000)
        selected_scooter.battery_capacity = new_battery_capacity
        try:
            self.context.user_repo.edit_scooter(selected_scooter, "battery_capacity", new_battery_capacity)
            print(f"Battery capacity updated to {new_battery_capacity}")
        except Exception as e:
            print(f"[✖] Error updating battery capacity: {e}")



    def edit_brand(self, selected_scooter: Scooter):
        if self.context.role != "system_admin" and self.context.role != "super_admin":
            print("You do not have permission to edit brand.")
            return
        
        new_brand = input("Enter new brand: ")
        if validate_brand(new_brand):
            selected_scooter.brand = new_brand
            try:
                self.context.user_repo.edit_scooter(selected_scooter, "brand", new_brand)
                print(f"Brand updated to {new_brand}")
            except Exception as e:
                print(f"[✖] Error updating brand: {e}")
        else:
            print("Invalid format of brand. Please try again")
            self.edit_brand(selected_scooter)


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
            return

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
            return
            
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
            return
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