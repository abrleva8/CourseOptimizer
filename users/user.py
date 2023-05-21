from exceptions import login_exception


class User:
    def __init__(self, login, password):
        self.login = login
        self.password = password

    def get_data(self):
        with open('C:\\Users\\abrle\\PycharmProjects\\CourseOptimizer\\users\\1.txt', 'r') as f:
            lines = f.readlines()
            for line in lines[1:]:
                login, password = map(str.rstrip, line.split(','))
                if login.__eq__(self.login):
                    if not password.__eq__(self.password):
                        raise login_exception.BadPasswordException(self.login)
                    else:
                        return self.login
            raise login_exception.NotSuchUserException(self.login)
