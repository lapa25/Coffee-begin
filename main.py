import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
import sqlite3
from PyQt5 import uic


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.conn = sqlite3.connect('coffee.sqlite')
        self.pushButton.clicked.connect(self.run)

    def run(self):
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(
            ['ID', 'название сорта', 'степень обжарки',
             'молотый/в зернах', 'описание вкуса', 'цена', 'объем упаковки'])
        self.tableWidget.setRowCount(0)
        request = "SELECT name.id,\n"
        request += "name.title, \n"
        request += "roasting.roasting, \n"
        request += "type.type, \n"
        request += "taste.about, \n"
        request += "price.price, \n"
        request += "volume.volume \n"
        request += "from name \n"
        request += "LEFT JOIN roasting ON name.id = roasting.id \n"
        request += "LEFT JOIN type ON name.id = type.id \n"
        request += "LEFT JOIN taste ON name.id = taste.id \n"
        request += "LEFT JOIN price ON name.id = price.id \n"
        request += "LEFT JOIN volume ON name.id = volume.id \n"
        request += "ORDER BY name.id;"
        cur = self.conn.cursor()
        res = cur.execute(request).fetchall()
        for i in range(len(res)):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j in range(7):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(res[i][j])))
        self.tableWidget.resizeColumnsToContents()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MyWidget()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())