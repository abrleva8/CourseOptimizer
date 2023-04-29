class LoginException(Exception):
    pass


class NotSuchUserException(LoginException):
    def __init__(self, login):
        super().__init__()
        self.login = login

    def __str__(self):
        return f"Логин {self.login} не найден"

    # def __str__(self):
    #     return repr(self.login)


class BadPasswordException(LoginException):
    def __init__(self, login):
        super().__init__()
        self.login = login

    def __str__(self):
        return f"Неправильно виден пароль для пользователя {self.login}"
