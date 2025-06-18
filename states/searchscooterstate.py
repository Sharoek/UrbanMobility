from .appstate import AppState

class searchScooterState(AppState):
    def __init__(self, context):
        super().__init__(context)

    def run(self):
        print("SEARCHING SCOOTERS")
        search_key = input(f"Input the search key: ")
        self.context.user_repo.search_scooter(search_key)   

