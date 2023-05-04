from exceptions import loginException
from test.user import User


class UserWorker:
    def __init__(self, login, password):
        self.user = User(login, password)

    def get_login(self):
        try:
            res = self.user.get_data()
        except loginException.LoginException as e:
            raise e

        return res
