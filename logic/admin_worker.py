import database

from exceptions import *


class AdminWorker:
    def __init__(self):
        self.admin_bd = database.admin_bd.DataBaseWorker()

    def get_methods(self):
        return self.admin_bd.get('name', 'method')

    def get_variations(self):
        return self.admin_bd.get('name', 'variation')

    def insert_method(self, name, elements):
        if name in elements:
            raise SameMethodException(name)
        self.admin_bd.insert(name, 'method')

    def insert_variation(self, name, elements):
        if name in elements:
            raise SameVariantException(name)
        self.admin_bd.insert(name, 'variation')

    def delete_method(self, name):
        if name == 'Метод Нелдер - Мида':
            raise NelderMeadException(name)
        self.admin_bd.delete(name, 'method')

    def delete_variation(self, name):
        if name == 'Абрамян':
            raise AbramyanException(name)
        self.admin_bd.delete(name, 'variation')


if __name__ == '__main__':
    a = AdminWorker()
    # l = a.get_methods()
