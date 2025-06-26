from encryption.validators import verify_number_input
from states.appstate import AppState
from log.manager import LogManager

class deleteTravellerState(AppState):
    def __init__(self, context):
        super().__init__(context)
        self.log_manager = LogManager()

    def run(self):
        print("\n-- Delete Traveller --")
        try:
            encrypted_travellers = self.context.admin_repo.get_all_travellers()
            travellers = self.context.admin_repo.decrypt_travellers(encrypted_travellers)
            for i, traveller in enumerate(travellers, start=1):
                print(f"{i}. {traveller['first_name']} {traveller['last_name']}")
            print("0. Exit")
            choice = verify_number_input("Select a traveller to delete: ", 0, len(travellers))
            if choice == 0:
                self.context.go_back()
                return
            else:
                traveller = travellers[int(choice) - 1]
                self.context.admin_repo.delete_traveller(traveller['customer_id'])
                self.log_manager.log(self.context.username, "Traveller deleted ", f"Traveller deleted: {traveller['first_name']}")
                self.context.go_back()
        except Exception as e:
            print(f"An error occurred: {e}")
            self.context.go_back()
            return