from menus.serviceEngineer_menu import serviceEngineerMenu
from menus.super_admin_menu import SuperAdminMenu
from menus.systemAdmin_menu import systemAdminMenu
from states.appstate import AppState

class MenuState(AppState):
    def run(self):
        role = self.context.role
        username = self.context.username
        if role == "super_admin":
            SuperAdminMenu(username, self.context).run()
        elif role == "system_admin":
            systemAdminMenu(username, self.context).run()
        elif role == "service_engineer":
            serviceEngineerMenu(username, self.context).run()
        else:
            print("Unknown role. Access denied.")
        # After the menu ends, return to login or terminate
        self.context.set_state(None)