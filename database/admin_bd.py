import mysql.connector


class DataBaseWorker:
    def __init__(self):
        self.connector = mysql.connector

    def get_methods(self) -> list:
        self._connect()
        my_cursor = self.connection.cursor()
        my_cursor.execute("SELECT name, available FROM method")
        result = my_cursor.fetchall()
        self.connection.close()
        return result

    def insert_method(self, name):
        self._connect()
        my_cursor = self.connection.cursor()
        query = f'INSERT method(name) VALUES ("{name}");'
        my_cursor.execute(query)
        self.connection.commit()
        self.connection.close()

    def delete_method(self, name):
        self._connect()
        my_cursor = self.connection.cursor()
        query = f'DELETE FROM method WHERE name="{name}";'
        my_cursor.execute(query)
        self.connection.commit()
        self.connection.close()

    def _connect(self):
        self.connection = self.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password='31August2008',
            database='optimizers'
        )


if __name__ == '__main__':
    db = DataBaseWorker()
    a = db.get_methods()
