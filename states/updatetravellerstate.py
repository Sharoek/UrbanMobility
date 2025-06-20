from states.appstate import AppState
from encryption.validators import get_valid_input, valid_housenumber, validate_driving_license, validate_email, validate_mobile, validate_name, validate_street, validate_zip_code, verify_number_input
from log.manager import LogManager

class updateTravellerState(AppState):
    def __init__(self, context):
        super().__init__(context)
        self.log_manager = LogManager()

    def run(self):
        self.print_select_travellers()

    def print_select_travellers(self):
        print("\n-- Update Traveller --")
        try:
            encrypted_travellers = self.context.admin_repo.get_all_travellers()
            travellers = self.context.admin_repo.decrypt_travellers(encrypted_travellers)
            for i, traveller in enumerate(travellers, start=1):
                print(f"{i}. {traveller['first_name']} {traveller['last_name']}")
            print("0. Exit")
            choice = verify_number_input("Select a traveller to update: ", 0, len(travellers))
            if choice == 0:
                self.context.go_back()
                return
            else:
                traveller = travellers[int(choice) - 1]
                self.print_update_menu(traveller)


        except Exception as e:
            print(f"An error occurred: {e}")
            self.context.go_back()
            return
        
    def print_update_menu(self, traveller):
        print("\n-- Update Traveller --")
        print("1. First name")
        print("2. Last name")
        print("3. Gender")
        print("4. Street name")
        print("5. House number")
        print("6. Zip code")
        print("7. City")
        print("8. Email address")
        print("9. Mobile phone")
        print("10. Driving license number")
        print("0. Exit")
        choice = verify_number_input("Select an option to update: ", 0, 10)
        if choice == 0:
            return
        elif choice == 1:
            try:
                first_name = get_valid_input("Enter first name: ", validate_name, "At least 2 characters, letters only", username=self.context.username)
                self.context.admin_repo.update_traveller(traveller["customer_id"], "first_name", first_name)
                self.log_manager.log(self.context.username, "First name updated", f"Traveller updated: {traveller['first_name']}")
                self.print_update_menu(traveller)
            except Exception as e:
                print(f"An error occurred: {e}")
                return
        elif choice == 2:
            try:
                last_name = get_valid_input("Enter last name: ", validate_name, "At least 2 characters, letters only", username=self.context.username)
                self.context.admin_repo.update_traveller(traveller["customer_id"], "last_name", last_name)
                self.log_manager.log(self.context.username, "Last name updated", f"Traveller updated: {traveller['first_name']}")
                self.print_update_menu(traveller)
            except Exception as e:
                print(f"An error occurred: {e}")
                return
        elif choice == 3:
            try:
                gender = self.select_gender()
                self.context.admin_repo.update_traveller(traveller["customer_id"], "gender", gender)
                self.log_manager.log(self.context.username, "Gender updated", f"Traveller updated: {traveller['first_name']}")
                self.print_update_menu(traveller)
            except Exception as e:
                print(f"An error occurred: {e}")
                return
        elif choice == 4:
            try:
                street = get_valid_input("Enter street name: ", validate_street, "Invalid street name", username=self.context.username)
                self.context.admin_repo.update_traveller(traveller["customer_id"],"street_name", street)
                self.log_manager.log(self.context.username, "Street name updated", f"Traveller updated: {traveller['first_name']}")
                self.print_update_menu(traveller)
                return
            except Exception as e:
                print(f"An error occurred: {e}")
                return
        elif choice == 5:
            try:
                house_number = get_valid_input("Enter house number: ", valid_housenumber, "Invalid house number", username=self.context.username)
                self.context.admin_repo.update_traveller(traveller["customer_id"], "house_number", house_number)
                self.log_manager.log(self.context.username, "House number updated", f"Traveller updated: {traveller['first_name']}")
                self.print_update_menu(traveller)
            except Exception as e:
                print(f"An error occurred: {e}")
                return
        elif choice == 6:
            try:
                zip_code = get_valid_input("Enter zip code: ", validate_zip_code, "Invalid zip code", username=self.context.username)
                self.context.admin_repo.update_traveller(traveller["customer_id"], "zip_code", zip_code)
                self.log_manager.log(self.context.username, "Zip code updated", f"Traveller updated: {traveller['first_name']}")
                self.print_update_menu(traveller)
            except Exception as e:
                print(f"An error occurred: {e}")
                return
        elif choice == 7:
            try:
                city = self.select_city()
                self.context.admin_repo.update_traveller(traveller["customer_id"],"city", city)
                self.log_manager.log(self.context.username, "City updated", f"Traveller updated: {traveller['first_name']}")
                self.print_update_menu(traveller)
            except Exception as e:
                print(f"An error occurred: {e}")
                return
        elif choice == 8:
            try:
                email_address = get_valid_input("Enter email address: ", validate_email, "Invalid email address", username=self.context.username)
                self.context.admin_repo.update_traveller(traveller["customer_id"],"email_address", email_address)
                self.log_manager.log(self.context.username, "Email address updated", f"Traveller updated: {traveller['first_name']}")
                self.print_update_menu(traveller)
            except Exception as e:
                print(f"An error occurred: {e}")
                return
        elif choice == 9:
            try:
                mobile_phone = get_valid_input("Enter mobile phone: ", validate_mobile, "Invalid mobile phone", username=self.context.username)
                self.context.admin_repo.update_traveller(traveller["customer_id"],"mobile_phone", mobile_phone)
                self.log_manager.log(self.context.username, "Mobile phone updated", f"Traveller updated: {traveller['first_name']}")
                self.print_update_menu(traveller)
            except Exception as e:
                print(f"An error occurred: {e}")
                return
        elif choice == 10:
            try:
                driving_license_number = get_valid_input("Enter driving license number: ", validate_driving_license, "Invalid driving license number", username=self.context.username)
                self.context.admin_repo.update_traveller(traveller["customer_id"], "driving_license_number", driving_license_number)
                self.log_manager.log(self.context.username, "Driving license number updated", f"Traveller updated: {traveller['first_name']}")
                self.print_update_menu(traveller)
            except Exception as e:
                print(f"An error occurred: {e}")
                return
        else:
            print("Invalid choice. Please try again.")
            self.print_update_menu(traveller)
    
    def select_gender(self):
        print("\nSelect gender:")
        print("1. Male")
        print("2. Female")
        choice = verify_number_input("Enter your choice: ", 1, 2)
        if choice == 1:
            return "male"
        elif choice == 2:
            return "female"
        else:
            print("Invalid choice. Please try again.")
            return self.select_gender()
    
    def select_city(self):
        print("Select City:\n")
        print("1. Amsterdam")
        print("2. Rotterdam")
        print("3. Utrecht")
        print("4. Eindhoven")
        print("5. Tilburg")
        print("6. Groningen")
        print("7. Breda")
        print("8. Enschede")
        print("9. Leiden")
        print("10. Maastricht")
        choice = verify_number_input("Enter your choice: ", 1, 10)
        if choice == 1:
            self.log_manager.log(self.context.username, "Amsterdam", "City selected")
            return "Amsterdam"
        if choice == 2:
            self.log_manager.log(self.context.username, "Rotterdam", "City selected")
            return "Rotterdam"
        if choice == 3:
            self.log_manager.log(self.context.username, "Utrecht", "City selected")
            return "Utrecht"
        if choice == 4:
            self.log_manager.log(self.context.username, "Eindhoven", "City selected")
            return "Eindhoven"
        if choice == 5:
            self.log_manager.log(self.context.username, "Tilburg", "City selected")
            return "Tilburg"
        if choice == 6:
            self.log_manager.log(self.context.username, "Groningen", "City selected")
            return "Groningen"
        if choice == 7:
            self.log_manager.log(self.context.username, "Breda", "City selected")
            return "Breda" 
        if choice == 8:
            self.log_manager.log(self.context.username, "Enschede", "City selected")
            return "Enschede"
        if choice == 9:
            self.log_manager.log(self.context.username, "Leiden", "City selected")
            return "Leiden"
        if choice == 10:
            self.log_manager.log(self.context.username, "Maastricht", "City selected")
            return "Maastricht"