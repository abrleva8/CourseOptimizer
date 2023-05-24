import sys

from PyQt6.QtWidgets import QApplication, QTableWidgetItem, QTableWidget, QWidget, QDialog


# data = {'col1': ['1', '2', '3', '4'],
#         'col2': ['1', '2', '1', '3'],
#         'col3': ['1', '1', '2', '1']}


class MyTableView(QDialog):
    def __init__(self, data, *args):
        super().__init__()
        self.table_widget = QTableWidget(*args)
        self.data = data
        self.set_data()
        self.table_widget.resizeColumnsToContents()
        self.table_widget.resizeRowsToContents()
        self.table_widget.show()
        i = 0

    def set_data(self):
        hor_headers = ['Первая вершина', 'Вторая вершина', 'Третья вершина']
        for index, value in enumerate(self.data):
            # hor_headers.append(str(index))
            for i, item in enumerate(value):
                item = tuple(map(lambda x: round(x, 2), item))
                new_item = QTableWidgetItem(str(item))
                self.table_widget.setItem(index, i, new_item)
        self.table_widget.setHorizontalHeaderLabels(hor_headers)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TableView(data, 4, 3)
    window.show()

    app.exec()
