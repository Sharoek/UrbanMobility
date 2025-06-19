from menus.base_menu import BaseMenu
from states.updatepasswordstate import UpdatePasswordState
from states.editscooterstate import editScooterState
from states.searchscooterstate import searchScooterState

class systemAdminMenu(BaseMenu):
    #Same as Service Engineer: 
    # • To update their own password. 
    # • To update the attributes of scooters in the system 
    # • To search and retrieve the information of a scooter (check note 2 below) 
    # Specific for the System Administrator: 
    # • To check the list of users and their roles. 
    # • To add a new Service Engineer to the system. 
    # • To update an existing Service Engineer account and profile. 
    # • To delete an existing Service Engineer account. 
    # • To reset an existing Service Engineer password (a temporary password). 
    # • To update his own account and profile. 
    # • To delete his own account. 
    # • To make a backup of the backend system. 
    # • To restore a specific backup of the backend system. For this purpose, the Super 
    # Administrator has generated a specific ‘one-use only’ code to restore a specific backup. 
    # • To see the logs file(s) of the backend system. 
    # • To add a new Traveller to the backend system. 
    # • To update the information of a Traveller in the backend system. 
    # • To delete a Traveller record from the backend system. 
    # • To add a new scooter to the backend system. 
    # • To update the information of a scooter in the backend system. 
    # • To delete a scooter from the backend system. 
    # • To search and retrieve the information of a Traveller (check note 2 below).
    def __init__(self, username, context):
        super().__init__(username, context)
        self.menu_options = {
            "0": "Logout",
            "1": "Update Password",
            "2": "Update Scooter Attributes",
            "3": "Search Scooter Information",
            "4": "Check User List and Roles",
            "5": "Add Service Engineer",
            "6": "Update Service Engineer Account",
            "7": "Delete Service Engineer Account",
            "8": "Reset Service Engineer Password",
            "9": "Update Own Account and Profile",
            "10": "Delete Own Account",
            "11": "Backup System",
            "12": "Restore Backup with Code",
            "13": "View Logs File(s)",
            "14": "Add Traveller",
            "15": "Update Traveller Information",
            "16": "Delete Traveller Record",
            "17": "Add Scooter",
            "18": "Update Scooter Information",
            "19": "Delete Scooter",
            "20": "Search Traveller Information"
        }
        self.menu_title = f"System Admin Menu - Logged in as: {self.username}"

    def show_options(self):
        print(self.menu_title)
        for key, value in self.menu_options.items():
            print(f"{key}. {value}")
    
    def handle_choice(self, choice):
        if choice == 0:
            exit() # Exit the menu and go back to the previous state
        if choice == 1:
            return UpdatePasswordState(self.context)
        elif choice == 2:
            return editScooterState(self.context)
        elif choice == 3:
            return searchScooterState(self.context)
        elif choice == "4":
            print("Checking user list and roles...")
            # Logic to check user list and roles
        elif choice == "5":
            print("Adding Service Engineer...")
            # Logic to add Service Engineer
        elif choice == "6":
            print("Updating Service Engineer account...")
            # Logic to update Service Engineer account
        elif choice == "7":
            print("Deleting Service Engineer account...")
            # Logic to delete Service Engineer account
        elif choice == "8":
            print("Resetting Service Engineer password...")
            # Logic to reset Service Engineer password
        elif choice == "9":
            print("Updating own account and profile...")
            # Logic to update own account and profile
        elif choice == "10":
            print("Deleting own account...")
            # Logic to delete own account
        elif choice == "11":
            print("Backing up system...")
            # Logic to backup system
        elif choice == "12":
            print("Restoring backup with code...")
            # Logic to restore backup with code
        elif choice == "13":
            print("Viewing logs file(s)...")
            # Logic to view logs file(s)
        elif choice == "14":
            print("Adding Traveller...")
            # Logic to add Traveller
        elif choice == "15":
            print("Updating Traveller information...")
            # Logic to update Traveller information
        elif choice == "16":
            print("Deleting Traveller record...")
            # Logic to delete Traveller record
        elif choice == "17":
            print("Adding Scooter...")
            # Logic to add Scooter
        elif choice == "18":
            print("Updating Scooter information...")
            # Logic to update Scooter information
        elif choice == "19":
            print("Deleting Scooter...")
            # Logic to delete Scooter
        elif choice == "20":
            print("Searching Traveller information...")
            # Logic to search Traveller information
        else:
            print("Invalid choice. Please try again.")