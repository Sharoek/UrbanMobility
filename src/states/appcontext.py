from states.loginstate import LoginState

class AppContext:
    def __init__(self):
        self.state = LoginState(self)
        self.username = None
        self.role = None
        self.user_repo = None
        self.previous_state = LoginState(self)
        self.admin_repo = None

    def set_state(self, state):
        self.previous_state = self.state
        self.state = state

    def go_back(self):
        self.state = self.previous_state


    def run(self):
        while self.state:
            self.state.run()