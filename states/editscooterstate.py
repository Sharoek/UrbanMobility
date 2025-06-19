from states.appstate import AppState
from encryption.validators import verify_number_input
from states.scootersubmenustate import scooterSubMenuState



class editScooterState(AppState):
    def run(self):
        self.display_scooter_list()   
        self.context.set_state(editScooterState(self.context))


    def display_scooter_list(self):
        print("Displaying scooters:")
        count = 1
        scooters = self.context.user_repo.get_scooters()
        for scooter in scooters:
            print(f"{count}. ID: {scooter.id}, Model: {scooter.model}, Brand: {scooter.brand}")
            count += 1    
        print("0. Go Back")    
        print("\nSelect an option:")
        choice = verify_number_input("Enter your choice:", 0, len(scooters))   
        if choice == 0:
            return self.context.go_back() 
        try:
            selected_scooter = scooters[choice - 1]
            print(f"You selected: {selected_scooter.model} ({selected_scooter.brand})")
            self.context.set_state(scooterSubMenuState(self.context, selected_scooter))
            self.context.run()
        except IndexError:
            print("Invalid choice. Please try again.")
            return self.display_scooter_list()