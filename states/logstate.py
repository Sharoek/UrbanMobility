from states.appstate import AppState
from log.manager import LogManager

class logState(AppState):
    """The blueprint of this class is to decrypt the log file and print it out to the gui in the following format:
        No.| Date | Time | Username | Description of Activity | Additional Information | Suspicious
    """

    def run(self):
        if self.context.role == "system_admin" or self.context.role == "super_admin":    
            log_manager = LogManager()
            logs = log_manager.read_logs()

            if not logs:
                print("\n📂 No logs to display.")
                return

            print("\nNo.|     Date     |  Time  | Username | Description               | Additional Info        | Suspicious")
            print("----|--------------|--------|----------|----------------------------|-------------------------|------------")
            for i, log in enumerate(logs, start=1):
                print(f"{i:<3} | {log['date']} | {log['time']} | {log['username']:<8} | {log['activity'][:26]:<26} | {log['info'][:23]:<23} | {'YES' if log['suspicious'] else 'NO '}")

            input("\nPress Enter to return to the menu...")


        else:
            print("You do not have permission to view logs.")
            return
