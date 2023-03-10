class Username:
    def __init__(self, state=0):
        self.state = state
        self.email = ""
        self.password = ""

    def get_info(self):
        return "email: {}\npassword: {}".format(self.email, self.password)
