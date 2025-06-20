from states.appstate import AppState
from models.traveller import Traveller
from encryption.validators import get_valid_input, verify_number_input, validate_name, validate_birthday, validate_birthday_range, validate_street, valid_housenumber,validate_mobile, validate_driving_license, validate_zip_code, validate_email
from database.seederRepository import seederRepository

from log.manager import LogManager

class addTravellerState(AppState):
    def __init__(self, context):
        super().__init__(context)
        self.log_manager = LogManager()
        self.seeder_repository = seederRepository()

    def run(self):
        self.add_traveller()
    
    def add_traveller(self):
        print("\n👤 Add Traveller:")

        traveller = Traveller(
            first_name="",
            last_name="",
            birthday="",
            gender="",
            street_name="",
            house_number="",
            zip_code="",
            city="",
            email_address="",
            mobile_phone="",
            driving_license_number=""
        )
        try:
            first_name = get_valid_input("Enter first name: ", validate_name, "At least 2 characters, letters only", username=self.context.username)
            if first_name:
                traveller.first_name = first_name
            last_name = get_valid_input("Enter last name: ", validate_name, "At least 2 characters, letters only", username=self.context.username)
            if last_name:
                traveller.last_name = last_name

            birthday = get_valid_input("Enter birthday: ", validate_birthday, "Invalid birthday: valid = YYYY-MM-DD", username=self.context.username)
            valid_birthday = validate_birthday_range(birthday)
            while valid_birthday == False:
                print("Birthday out of range")
                self.log_manager.log(self.context.username, "Invalid birthday entries", "Invalid birthday entries", True)
                birthday = get_valid_input("Enter birthday: ", validate_birthday, "Invalid birthday: valid = YYYY-MM-DD", username=self.context.username)
                valid_birthday = validate_birthday_range(birthday)

            if valid_birthday != False:
                traveller.birthday = birthday


            gender = self.select_gender()
            if gender:
                traveller.gender = gender
            else:
                self.log_manager.log(self.context.username, "invalid gender entries", "", True)
            street = get_valid_input("Enter street name: ", validate_street, "Invalid street name", username=self.context.username)
            if street:
                traveller.street_name = street
            house_number = get_valid_input("Enter house number: ", valid_housenumber, "Invalid house number", username=self.context.username)
            if house_number:
                traveller.house_number = house_number
            zip_code = get_valid_input("Enter zip code: ", validate_zip_code, "Invalid zip code", username=self.context.username)
            if zip_code:
                traveller.zip_code = zip_code
            city = self.select_city()
            if city:
                traveller.city = city
            else:
                "Something went wrong"
            email = get_valid_input("Enter email address: ", validate_email, "Invalid email address", username=self.context.username)
            if email:
                traveller.email_address = email
            mobile = get_valid_input("Enter mobile phone: +31-6", validate_mobile, "Invalid mobile phone", username=self.context.username)
            if mobile:
                traveller.mobile_phone = mobile
            driving_license_number = get_valid_input("Enter driving license number: ", validate_driving_license, "Invalid driving license number: Format: XDDDDDDDD or XXDDDDDDD", username=self.context.username)
            if driving_license_number:
                traveller.driving_license_number = driving_license_number
            
            self.seeder_repository.save_traveller_to_db(traveller)
            
        except Exception as e:
            print(f"Error: {e}")
            return False
        
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