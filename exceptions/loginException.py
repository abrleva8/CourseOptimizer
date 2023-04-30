class LoginException(Exception):
    pass


class NotSuchUserException(LoginException):
    def __init__(self, login):
        super().__init__()
        self.login = login

    def __str__(self):
        return f"Логин {self.login} не найден"


class BadPasswordException(LoginException):
    def __init__(self, login):
        super().__init__()
        self.login = login

    def __str__(self):
        return f"Неправильно введен пароль для пользователя {self.login}"
