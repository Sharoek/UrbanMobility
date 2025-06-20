from menus.base_menu import BaseMenu
from states.addscooterstate import addScooterState
from states.addtravellerstate import addTravellerState
from states.adduserstate import addUserState
from states.backupstate import BackupState
from states.deletescooterstate import deleteScooterState
from states.deletetravellerstate import deleteTravellerState
from states.deleteuserstate import deleteUserState
from states.editscooterstate import editScooterState
from states.logstate import logState
from states.resetuserpasswordstate import resetUserPasswordState
from states.restorecodestate import restoreCodeState
from states.searchscooterstate import searchScooterState
from states.searchtravellerstate import searchTravellerState
from states.updatetravellerstate import updateTravellerState
from states.updateuserstate import updateUserState
from states.viewusersstate import viewUsersState

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
            "5": "Update Service Engineer Accsount",
            "6": "Delete Service Engineer Account",
            "7": "Reset Service Engineer Password",
            "8": "View Logs File(s)",
            "9": "Add Traveller",
            "10": "Update Traveller Information",
            "11": "Delete Traveller Record",
            "12": "Add Scooter",
            "13": "Delete Scooter",
            "14": "Search Traveller Information",
            "15": "Add System Administrator",
            "16": "Update System Administrator Account",
            "17": "Delete System Administrator Account",
            "18": "Reset System Administrator Password",
            "19": "Backup System",
            "20": "Restore Backup with Code",
            "0": "Exit"
        }

    def show_options(self):
        for key, value in self.menu_options.items():
            print(f"{key}. {value}")
    
    def handle_choice(self, choice):
        if choice == 1:
            return editScooterState(self.context)
        elif choice == 2:
            return searchScooterState(self.context)
        elif choice == 3:
            return viewUsersState(self.context)
        elif choice == 4:
            return addUserState(self.context)
        elif choice == 5:
            return updateUserState(self.context)
        elif choice == 6:
            return deleteUserState(self.context) 
        elif choice == 7:
            return resetUserPasswordState(self.context)
        elif choice == 8:
            return logState(self.context)
        elif choice == 9:
            return addTravellerState(self.context)
        elif choice == 10:
            return updateTravellerState(self.context)
        elif choice == 11:
            return deleteTravellerState(self.context) 
        elif choice == 12:
            return addScooterState(self.context) 
        elif choice == 13:
            return deleteScooterState(self.context)
        elif choice == 14:
            return searchTravellerState(self.context)
        elif choice == 15:
            return addUserState(self.context, menu="system_admin")
        elif choice == 16:
            return updateUserState(self.context, menu="system_admin")
        elif choice == 17:
            return deleteUserState(self.context, menu="system_admin") 
        elif choice == 18:
            return resetUserPasswordState(self.context, user="system_admin")
        elif choice == 19:
            return BackupState(self.context)
        elif choice == 20:
            return restoreCodeState(self.context)
        elif choice == 0:
            exit()      
        else:
            print("Invalid choice. Please try again.")
            return None
