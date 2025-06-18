from menus.base_menu import BaseMenu
from states.updatepasswordstate import UpdatePasswordState
from states.editscooterstate import editScooterState
from states.searchscooterstate import searchScooterState

class serviceEngineerMenu(BaseMenu):
    def __init__(self, username, context):
        super().__init__(username, context)
        self.menu_options = {
            # • To update their own password
            # • To update some attributes of scooters in the system
            # • To search and retrieve the information of a scooter (check note 2 below)
            "0": "Logout",
            "1": "Update Own Password",
            "2": "Update Scooter Attributes",
            "3": "Search Scooter Information",
        }
        self.menu_title = "Service Engineer Menu"
    
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
        else:
            print("Invalid choice. Please try again.")
            return True

 