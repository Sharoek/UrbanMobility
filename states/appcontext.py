from states.loginstate import LoginState

class AppContext:
    def __init__(self):
        self.state = LoginState(self)
        self.username = None
        self.role = None
        self.user_repo = None

    def set_state(self, state):
        self.state = state

    def run(self):
        while self.state:
            self.state.run()