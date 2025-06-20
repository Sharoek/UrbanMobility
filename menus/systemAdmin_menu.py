from menus.base_menu import BaseMenu
from states.addtravellerstate import addTravellerState
from states.backupstate import BackupState
from states.deleteuserstate import deleteUserState
from states.logstate import logState
from states.resetuserpasswordstate import resetUserPasswordState
from states.searchtravellerstate import searchTravellerState
from states.updatepasswordstate import UpdatePasswordState
from states.editscooterstate import editScooterState
from states.searchscooterstate import searchScooterState
from states.updateuserstate import updateUserState
from states.viewusersstate import viewUsersState
from states.adduserstate import addUserState

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
            "12": "View Logs File(s)",
            "13": "Add Traveller",
            "14": "Update Traveller Information",
            "15": "Delete Traveller Record",
            "16": "Add Scooter",
            "17": "Update Scooter Information",
            "18": "Delete Scooter",
            "19": "Search Traveller Information"
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
        elif choice == 4:
            return viewUsersState(self.context)
        elif choice == 5:
            return addUserState(self.context)
        elif choice == 6:
            return updateUserState(self.context)
        elif choice == 7:
            return deleteUserState(self.context)    
        elif choice == 8:
            return resetUserPasswordState(self.context)
        elif choice == 9:
            return updateUserState(self.context, True)
        elif choice == 10:
            return deleteUserState(self.context, True)
        elif choice == 11:
            return BackupState(self.context)    ## needs to be triple checked
        elif choice == 12:
            return logState(self.context)
        elif choice == 13:
            return addTravellerState(self.context)
        elif choice == "14":
            print("Updating Traveller information...")
            # Logic to update Traveller information
        elif choice == "15":
            print("Deleting Traveller record...")
            # Logic to delete Traveller record
        elif choice == "16":
            print("Adding Scooter...")
            # Logic to add Scooter
        elif choice == "17":
            print("Updating Scooter information...")
            # Logic to update Scooter information
        elif choice == "18":
            print("Deleting Scooter...")
            # Logic to delete Scooter
        elif choice == 19:
            return searchTravellerState(self.context)
            
        else:
            print("Invalid choice. Please try again.")