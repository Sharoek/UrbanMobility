from .appstate import AppState

class searchTravellerState(AppState):
    def run(self):
        print("SEARCHING Travellers")
        search_key = input(f"Input the search key: ")
        self.context.admin_repo.search_traveller(search_key)   

