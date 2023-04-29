from exceptions import loginException


class User:
    def __init__(self, login, password):
        self.login = login
        self.password = password

    def get_data(self):
        with open('1.txt') as f:
            lines = f.readlines()
            for line in lines[1:]:
                login, password = line.split(',')
                if not login.__eq__(self.login):
                    if not password.__eq__(self.password):
                        raise loginException.BadPasswordException(login)
            raise loginException.NotSuchUserException(login)

        return self.login
