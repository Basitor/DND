import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QInputDialog, QMessageBox)


class Main_UI(QMainWindow):
    heroName = ''

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Generating the main menu buttons
        count = 1
        Buttons = ['New item', 'Delete item', 'Change the item holder']

        for item in Buttons:
            new_button = QPushButton(item, self)
            new_button.move(20, 30 * count)
            new_button.resize(140, 30)
            new_button.clicked.connect(self.buttonClicked)
            count += 1

        self.setGeometry(300, 300, 180, 200)
        self.setWindowTitle('Items Changing')
        self.show()

    def buttonClicked(self):
        # Parsing the pressed button
        sender = self.sender()
        if sender.text() == 'Delete item':
            self.deleteAnItem()
        elif sender.text() == 'New item':
            self.createNewItem()
        elif sender.text() == 'Change the item holder':
            self.changeItemHolder()

    # If the Delete item button was pressed
    def deleteAnItem(self):

        # Generating the variables
        list_of_items, items = [], []
        item_name = ''

        # Connecting to the SQL
        connection = sqlite3.connect("company.db")
        cursor = connection.cursor()

        # Getting the list of items
        cursor.execute("SELECT item_name FROM Item")
        list_of_items = cursor.fetchall()
        for i in list_of_items:
            items.append(i[0])

        # Selecting the item
        text, ok = QInputDialog.getItem(self, 'Input Dialog', 'Hero name:', items, 0, False)
        if ok:
            item_name = text

        # Deleting the item from DB
        cursor.execute("""DELETE FROM Item WHERE item_name="{}";""".format(item_name))
        connection.commit()
        connection.close()

    # If the New Item button was pressed
    def createNewItem(self):

        # Generating the variables
        self.heroName = ''
        hero_list = []
        stats_list = ['STR', 'AGI', 'INT']
        item_stats = []
        itemName, itemDescr = "", ""

        # Connecting to the SQL
        connection = sqlite3.connect("company.db")
        cursor = connection.cursor()

        # Getting the list of hero names from DB
        cursor.execute("SELECT hero_name FROM Hero")
        list_of_heroes = cursor.fetchall()
        for i in list_of_heroes:
            hero_list.append(i[0])
        hero_list.append('***NEW HERO***')
        hero_list.append('No holder')

        # Getting the hero name from user
        text, ok = QInputDialog.getItem(self, 'Input Dialog', 'Hero name:', hero_list, 0, False)
        if ok:
            self.heroName = text

        # Getting the item name from user
        text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter item name:')
        if ok:
            itemName = text

        # Getting the description from user
        text, ok = QInputDialog.getMultiLineText(self, 'Input Dialog', 'Enter item description:')
        if ok:
            itemDescr = text

        # Getting the value for each stat from user
        for i in stats_list:
            text, ok = QInputDialog.getInt(self, 'Input Dialog', '{}:'.format(i))
            if ok:
                item_stats.append(str(text))

        # If this stat belongs to the new hero
        if self.heroName == '***NEW HERO***':
            while True:
                text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter hero name (the name should be new):')
                if ok and text not in hero_list:
                    self.heroName = text

                    # Commiting to the DB and closing the connection
                    cursor.execute("""INSERT INTO Hero (hero_number, hero_name)
                                    VALUES (NULL, "{}")""".format(self.heroName))
                    connection.commit()
                    connection.close()

                    # Connect to the SQL again
                    connection = sqlite3.connect("company.db")
                    cursor = connection.cursor()
                    break
                else:
                    QMessageBox.question(self, 'Message', "Hero name should be unique", QMessageBox.Yes | QMessageBox.Yes)
                    continue

        # Getting the ID of selected hero
        if self.heroName == 'No holder':
            HERO_ID = None
        else:
            # If someone should hold this item
            cursor.execute("""SELECT hero_number FROM Hero WHERE hero_name = "{}";""".format(self.heroName))
            HERO_ID = cursor.fetchone()[0]

        # Generating data for Inserting to SQL
        format_str = """INSERT INTO Item (item_number, item_name, item_descr, STR, AGI, MAGIC, hero_number)
                        VALUES (NULL, "{name}", "{descr}", "{STR}", "{AGI}", "{MAGIC}", "{hero}");"""
        sql_command = format_str.format(name=itemName, descr=itemDescr, STR=item_stats[0], AGI=item_stats[1],
                                        MAGIC=item_stats[2], hero=HERO_ID)
        # Commiting data to the DB
        cursor.execute(sql_command)
        connection.commit()

        # If item do not need a holder
        if HERO_ID is None:
            cursor.execute("""UPDATE Item SET hero_number=NULL""")
            connection.commit()
        connection.close()

    def changeItemHolder(self):
        # Setting variables
        listOfItems, listOfHeroes = [], []
        item_name, hero_name = '', ''

        # Connecting to the SQL
        connection = sqlite3.connect("company.db")
        cursor = connection.cursor()

        # Generating the list of items
        cursor.execute("""SELECT item_name FROM Item""")
        for i in cursor.fetchall():
            listOfItems.append(i[0])

        # Selecting the item
        text, ok = QInputDialog.getItem(self, 'Input Dialog', 'Select the item:', listOfItems, 0, False)
        if ok:
            item_name = text

        # Select a new holder
        cursor.execute("""SELECT hero_name FROM Hero""")
        for i in cursor.fetchall():
            listOfHeroes.append(i[0])
        listOfHeroes.append('***Stash the item***')

        # Selecting the holder and getting his ID
        text, ok = QInputDialog.getItem(self, 'Input Dialog', 'Select the hero:', listOfHeroes, 0, False)
        if ok and text != '***Stash the item***':
            hero_name = text
            cursor.execute("""SELECT hero_number FROM Hero WHERE hero_name = "{}";""".format(hero_name))
            hero_ID = cursor.fetchone()[0]
        else:
            hero_ID = None

        # Changing the holder
        if hero_ID is not None:
            cursor.execute("""UPDATE Item SET hero_number={} WHERE item_name="{}";""".format(hero_ID, item_name))
        else:
            cursor.execute("""UPDATE Item SET hero_number=NULL WHERE item_name="{}";""".format(item_name))

        # Applying the changes
        connection.commit()
        connection.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main_UI()
    sys.exit(app.exec_())
