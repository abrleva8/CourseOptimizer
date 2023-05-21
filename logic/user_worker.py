from exceptions import login_exception
from users.user import User


class UserWorker:
    def __init__(self, login, password):
        self.user = User(login, password)

    def get_login(self):
        try:
            res = self.user.get_data()
        except login_exception.LoginException as e:
            raise e

        return res
