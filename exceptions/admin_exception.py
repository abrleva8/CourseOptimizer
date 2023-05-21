class AdminException(Exception):
    pass


class NelderMeadException(AdminException):

    def __str__(self):
        return f"Метод Нелдер-Мида удалять нельзя!"


class SameMethodException(AdminException):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self):
        return f"Метод `{self.name}` уже есть в базе!"
