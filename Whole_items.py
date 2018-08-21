import sys
from PyQt5.QtWidgets import (QLabel, QApplication, QMainWindow)
from PyQt5.QtGui import QFont
import sqlite3


class Main_UI(QMainWindow):

    connection = sqlite3.connect("company.db")
    cursor = connection.cursor()

    # Collecting the list of heroes
    cursor.execute("SELECT Hero_name FROM Hero")
    list_of_heroes = cursor.fetchall()
    heroes = []
    for i in list_of_heroes:
        heroes.append(i[0])

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        count = 1
        count2 = 1
        ID = []
        Name = []

        # Generating the list of all items
        self.cursor.execute("""SELECT * FROM Item""")
        items = self.cursor.fetchall()

        # Getting the ID and name of each hero
        self.cursor.execute("""SELECT hero_number, hero_name FROM Hero""")
        for i in self.cursor.fetchall():
            ID.append(i[0])
            Name.append(i[1])
        idWithKeys = dict(zip(ID, Name))

        # Generating the headers
        New_item = QLabel("Unequipped items:", self)
        New_item.move(350, 30 * count2)
        New_item.setFont(QFont('ComicSans', 14))
        New_item.adjustSize()
        count2 += 1

        New_item = QLabel("Equipped items:", self)
        New_item.move(20, 30 * count)
        New_item.setFont(QFont('ComicSans', 14))
        New_item.adjustSize()
        count += 1

        # Generating the labels for each item
        for item in items:

            # If someone carrying the item
            if item[6] is not None:

                # Item name
                New_item = QLabel(item[1], self)
                New_item.move(20, 30 * count)
                New_item.setFont(QFont('SansSerif', 13))
                New_item.adjustSize()
                count += 1

                # Item description
                New_item = QLabel(item[2], self)
                New_item.move(20, 30 * count)
                New_item.adjustSize()
                count += 1

                # Item stats
                New_item = QLabel("STR = {}, AGI = {}, INT = {}".format(item[3], item[4], item[5]), self)
                New_item.move(20, 30 * count)
                New_item.adjustSize()
                count += 1

                # The name of the holder
                New_item = QLabel("Right now {} is using this item".format(idWithKeys[item[6]]), self)
                New_item.move(20, 30 * count)
                New_item.adjustSize()
                count += 1

            # If no one is carrying the item
            if item[6] is None:

                # Item name
                New_item = QLabel(item[1], self)
                New_item.move(350, 30 * count2)
                New_item.setFont(QFont('SansSerif', 13))
                New_item.adjustSize()
                count2 += 1

                # Item description
                New_item = QLabel(item[2], self)
                New_item.move(350, 30 * count2)
                New_item.adjustSize()
                count2 += 1

                # Item stats
                New_item = QLabel("STR = {}, AGI = {}, INT = {}".format(item[3], item[4], item[5]), self)
                New_item.move(350, 30 * count2)
                New_item.adjustSize()
                count2 += 1

                # The name of the holder
                New_item = QLabel("No one is using this item", self)
                New_item.move(350, 30 * count2)
                New_item.adjustSize()
                count2 += 1

        self.setGeometry(300, 300, 600, 800)
        self.setWindowTitle('Items Database')
        self.show()

        self.connection.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main_UI()
    sys.exit(app.exec_())