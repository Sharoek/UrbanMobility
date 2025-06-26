from .appstate import AppState

class searchScooterState(AppState):
    def run(self):
        print("SEARCHING SCOOTERS")
        search_key = input(f"Input the search key: ")
        self.context.user_repo.search_scooter(search_key)   

