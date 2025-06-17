from menus.base_menu import BaseMenu

class SuperAdminMenu(BaseMenu):
    # • To update the attributes of scooters in the system 
    # • To search and retrieve the information of a scooter 
    # • To check the list of users and their roles. 
    # • To add a new Service Engineer to the backend system. 
    # • To modify or update an existing Service Engineer account and profile. 
    # • To delete an existing Service Engineer account. 
    # • To reset an existing Service Engineer password (a temporary password). 
    # • To see the logs file(s) of the backend system. 
    # • To add a new Traveller to the backend system. 
    # • To update the information of a Traveller in the backend system. 
    # • To delete a Traveller from the backend system. 
    # • To add a new scooter to the backend system. 
    # • To update the information of a scooter in the backend system. 
    # • To delete a scooter from the backend system. 
    # • To search and retrieve the information of a Traveller (check note 2 below). 
    # Specific for the Super Administrator: 
    # • To add a new System Administrator to the backend system. 
    # • To modify or update an existing System Administrator account and profile. 
    # • To delete an existing System Administrator account. 
    # • To reset an existing System Administrator password (a temporary password). 
    # • To make a backup of the backend system and to restore a backup. 
    # • To allow a specific System Administrator to restore a specific backup. 
    # • To revoke a previously generated restore-code for a System Administrator. 
    def __init__(self, username, context):
        super().__init__(username, context)
        self.menu_options = {
            "1": "Update Scooter Attributes",
            "2": "Search Scooter Information",
            "3": "Check User List and Roles",
            "4": "Add Service Engineer",
            "5": "Update Service Engineer Account",
            "6": "Delete Service Engineer Account",
            "7": "Reset Service Engineer Password",
            "8": "View Logs File(s)",
            "9": "Add Traveller",
            "10": "Update Traveller Information",
            "11": "Delete Traveller Record",
            "12": "Add Scooter",
            "13": "Update Scooter Information",
            "14": "Delete Scooter",
            "15": "Search Traveller Information",
            "16": "Add System Administrator",
            "17": "Update System Administrator Account",
            "18": "Delete System Administrator Account",
            "19": "Reset System Administrator Password",
            "20": "Backup System",
            "21": "Restore Backup with Code"
        }
        self.menu_title = f"Super Admin Menu - Logged in as: {self.username}"

    def show_options(self):
        print(self.menu_title)
        for key, value in self.menu_options.items():
            print(f"{key}. {value}")
    
    def handle_choice(self, choice):
        if choice == "1":
            print("Updating scooter attributes...")
            # Logic to update scooter attributes
        elif choice == "2":
            print("Searching scooter information...")
            # Logic to search scooter information
        elif choice == "3":
            print("Checking user list and roles...")
            # Logic to check user list and roles
        elif choice == "4":
            print("Adding Service Engineer...")
            # Logic to add Service Engineer
        elif choice == "5":
            print("Updating Service Engineer account...")
            # Logic to update Service Engineer account
        elif choice == "6":
            print("Deleting Service Engineer account...")
            # Logic to delete Service Engineer account
        elif choice == "7":
            print("Resetting Service Engineer password...")
            # Logic to reset Service Engineer password
        elif choice == "8":
            print("Viewing logs file(s)...")
            # Logic to view logs file(s)
        elif choice == "9":
            print("Adding Traveller...")
            # Logic to add Traveller
        elif choice == "10":
            print("Updating Traveller information...")
            # Logic to update Traveller information
        elif choice == "11":
            print("Deleting Traveller record...")
            # Logic to delete Traveller record
        elif choice == "12":
            print("Adding Scooter...")
            # Logic to add Scooter
        elif choice == "13":
            print("Updating Scooter information...")
            # Logic to update Scooter information
        elif choice == "14":
            print("Deleting Scooter...")
            # Logic to delete Scooter
        elif choice == "15":
            print("Searching Traveller information...")
            # Logic to search Traveller information
        elif choice == "16":
            print("Adding System Administrator...")
            # Logic to add System Administrator
        elif choice == "17":
            print("Updating System Administrator account...")
            # Logic to update System Administrator account
        elif choice == "18":
            print("Deleting System Administrator account...")
            # Logic to delete System Administrator account
        elif choice == "19":
            print("Resetting System Administrator password...")
            # Logic to reset System Administrator password
        elif choice == "20":
            print("Backing up system...")
            # Logic to backup system
        elif choice == "21":
            print("Restoring backup with code...")
            # Logic to restore backup with code
        else:
            print("Invalid choice. Please try again.")
        
        return True
