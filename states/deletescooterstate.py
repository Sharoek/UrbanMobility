from states.appstate import AppState
from encryption.validators import verify_number_input
from log.manager import LogManager

class deleteScooterState(AppState):
    def __init__(self, context):
        super().__init__(context)
        self.log_manager = LogManager()


    def run(self):
        print("DELETING Scooter")
        self._printScooters()

    def _printScooters(self):
        index = 1
        print("\n-- Delete Scooter --")
        try:
            scooters = self.context.user_repo.get_scooters()
            for scooter in scooters:
                print(f"{index}. ID: {scooter.id}, Model: {scooter.model}, Out of serivce: {scooter.out_of_service_status}")
                index += 1
            print("0. Exit")
            choice = verify_number_input("Select a scooter to delete: ", 1, len(scooters))
            if choice == 0:
                self.context.go_back()
                return
            else:
                scooter_id = scooters[int(choice) - 1].id
                self.context.admin_repo.delete_scooter(scooter_id)
                self.log_manager.log(self.context.username, f"Scooter {scooter_id} deleted", "")
                print("✅ Scooter deleted successfully.")
                self.context.go_back()
                return
        except Exception as e:
            print(f"An error occurred: {e}")
            self.log_manager.log(self.context.username, f"Tried to delete scooter {scooter_id}", "")
            self.context.go_back()
            return