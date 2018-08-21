import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
    QTextEdit, QGridLayout, QApplication, QMainWindow, QPushButton, QInputDialog)
from PyQt5.QtGui import QFont
import sqlite3


class Main_UI(QMainWindow):
    current_hero = ''
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
        # Generating the main menu / selecting the hero
        item, okPressed = QInputDialog.getItem(self, "Hero", "Choose a hero:", self.heroes, 0, False)
        if okPressed and item:
            self.initData(item)

    def initData(self, hero):
        count = 0
        cursor = self.cursor

        self.current_hero = hero

        # Generating the list of heroes
        cursor.execute("""SELECT hero_number FROM Hero WHERE hero_name = "{}" """.format(hero))
        hero_ID = cursor.fetchone()[0]

        # Getting the list of items
        cursor.execute("""SELECT * FROM Item WHERE hero_number = {}""".format(int(hero_ID)))
        item_stats = cursor.fetchall()

        # Generating the data for each item
        for item in item_stats:
            if item[6] == hero_ID:

                # The name of the item
                New_item = QLabel(item[1], self)
                New_item.move(20, 30 * count)
                New_item.setFont(QFont('SansSerif', 13))
                New_item.adjustSize()
                count += 1

                # The description of the item
                New_item = QLabel(item[2], self)
                New_item.move(20, 30 * count)
                New_item.adjustSize()
                count += 1

                # The "Stats line"
                New_item = QLabel("Stats: ", self)
                New_item.move(20, 30 * count)
                count += 1

                stats_names = ["STR", "AGI", "INT"]
                stat_num = 3

                # Generating the label for each stat
                for j in range(3):

                    New_item = QLabel(str(stats_names[stat_num - 3]), self)
                    New_item.move(20, 30 * count)

                    New_item = QLabel(str(item[stat_num]), self)
                    New_item.move(80, 30 * count)
                    count += 1
                    stat_num += 1
                count += 1

        self.setGeometry(300, 300, 600, 800)
        self.setWindowTitle('Items Database')
        self.show()

        self.connection.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main_UI()
    sys.exit(app.exec_())
