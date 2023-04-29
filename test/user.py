from exceptions import loginException


class User:
    def __init__(self, login, password):
        self.login = login
        self.password = password

    def get_data(self):
        try:
            with open('C:\\Users\\abrle\\PycharmProjects\\CourseOptimizer\\test\\1.txt', 'r') as f:
                lines = f.readlines()
                for line in lines[1:]:
                    login, password = map(str.rstrip, line.split(','))
                    if login.__eq__(self.login):
                        if not password.__eq__(self.password):
                            raise loginException.BadPasswordException(login)
                        else:
                            return login
                raise loginException.NotSuchUserException(login)
        except ValueError:
            print(3)

        return self.login


User("", "")
