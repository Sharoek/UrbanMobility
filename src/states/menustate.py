from menus.serviceEngineer_menu import serviceEngineerMenu
from menus.super_admin_menu import SuperAdminMenu
from menus.systemAdmin_menu import systemAdminMenu
from states.appstate import AppState
from log.manager import LogManager
from encryption.validators import verify_number_input

class MenuState(AppState):
    def run(self):
        role = self.context.role
        username = self.context.username
        try:
            if role in ["super_admin", "system_admin"]:
                log_manager = LogManager()
                unread_logs = log_manager.get_unread_suspicious_logs()
                if unread_logs:
                    print(f"\n[⚠️] ALERT: You have {len(unread_logs)} unread suspicious activity log(s):\n")
                    for log in unread_logs:
                        print(f"- [{log['date']} {log['time']}] User: {log['username']} | Activity: {log['activity']} | Info: {log['info']}")
                    choice = verify_number_input("Do you want to mark all suspicious logs as read?\n1. Yes\n2. No\n", 1,2)
                    if choice == 1:
                        log_manager.mark_logs_as_read()
                        print("[✔] All suspicious logs marked as read.\n")
                    else:
                        print("[✔] No unread suspicious activities.\n")
        except Exception as e:
            print(f"[✖] Error checking suspicious logs: {e}")
            
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