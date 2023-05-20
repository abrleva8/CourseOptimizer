import database


class AdminWorker:
    def __init__(self):
        self.admin_bd = database.admin_bd.DataBaseWorker()

    def get_methods(self):
        return self.admin_bd.get_methods()

    def insert_method(self, name):
        self.admin_bd.insert_method(name)

    def delete_method(self, name):
        self.admin_bd.delete_method(name)


if __name__ == '__main__':
    a = AdminWorker()
    l = a.get_methods()
