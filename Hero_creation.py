import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QInputDialog)
import sqlite3

class Main_UI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    # Generating the main menu
    def initUI(self):

        count = 1
        Buttons = ['New hero', 'Delete hero', 'Cancel']

        # Creating the buttons
        for item in Buttons:
            new_button = QPushButton(item, self)
            new_button.move(20, 30 * count)
            new_button.resize(140, 30)
            new_button.clicked.connect(self.buttonClicked)
            count += 1

        # Creating the layout
        self.setGeometry(300, 300, 600, 800)
        self.setWindowTitle('Items Database')
        self.show()

    # Parsing the pressed button
    def buttonClicked(self):
        sender = self.sender()
        if sender.text() == 'New hero':
            self.newHero()
        elif sender.text() == 'Cancel':
            self.Cancel()
        elif sender.text() == 'Delete hero':
            self.DeleteHero()

    # Creating a new hero
    def newHero(self):
        # Setting the variables
        players, list_of_players, results, resultStats = [], [], [], []
        character = ['name', 'level', 'class', 'story', 'race', 'ideology', 'experience']
        stats = ['STR', 'AGI', 'Constitution', 'INT', 'WISDOM', 'CHARISMA']
        player_name = ''

        # Connecting to the DB
        connection = sqlite3.connect("company.db")
        cursor = connection.cursor()

        # Getting the Player names
        cursor.execute("SELECT player_name FROM Hero")
        list_of_players = cursor.fetchall()
        for i in list_of_players:
            players.append(i[0])
        players.append('***NEW PLAYER***')

        # Selecting the player name
        text, ok = QInputDialog.getItem(self, 'Input Dialog', 'The name of the player:', players, 0, False)
        if ok:
            player_name = text
        if player_name == '***NEW PLAYER***':
            text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter the name of a new player:')
            if ok:
                player_name = text

        # Creating the dialogues about the hero
        for item in character:
            if item == 'level' or item == 'experience':
                text, ok = QInputDialog.getInt(self, 'Input Dialog', 'Enter the {} of new hero:'.format(item))
                if ok:
                    results.append(text)
            else:
                text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter the {} of new hero:'.format(item))
                if ok:
                    results.append(text)

        for item in stats:
            text, ok = QInputDialog.getInt(self, 'Input Dialog', 'Enter the {} of new hero:'.format(item))
            if ok:
                resultStats.append(text)

        # Generating data for the DB (hero main characteristics)
        format_str = """INSERT INTO Hero (hero_number, hero_name, hero_level, hero_class, hero_story, hero_race, 
                                            hero_ideology, hero_experience, player_name)
                        VALUES (NULL, "{name}", {level}, "{clas}", "{story}", "{race}", 
                                            "{ideology}", "{exp}", "{player}");"""
        sql_command = format_str.format(name=results[0], level=results[1], clas=results[2], story=results[3],
                                        race=results[4], ideology=results[5], exp=results[5], player=player_name)

        # Commiting data to the DB
        cursor.execute(sql_command)
        connection.commit()

        # Generating data for the DB (hero stats)
        format_str = """INSERT INTO Hero_stats
                        VALUES (NULL, {STR}, {AGI}, {Constitution}, {INT}, {WISDOM}, {Charisma});"""
        sql_command = format_str.format(STR=resultStats[0], AGI=resultStats[0], Constitution=resultStats[0],
                                        INT=resultStats[0], WISDOM=resultStats[0], Charisma=resultStats[0])

        # Commiting data to the DB
        cursor.execute(sql_command)
        connection.commit()
        connection.close()

    def DeleteHero(self):
        heroes = []
        hero_name = ''

        # Connecting to the DB
        connection = sqlite3.connect("company.db")
        cursor = connection.cursor()

        # Getting the Player names
        cursor.execute("SELECT hero_name FROM Hero")
        list_of_players = cursor.fetchall()
        for i in list_of_players:
            heroes.append(i[0])

        # Selecting a hero for delete
        text, ok = QInputDialog.getItem(self, 'Input Dialog', 'The name of hero:', heroes, 0, False)
        if ok:
            hero_name = text

        # Deleting the data
        cursor.execute("""SELECT hero_number FROM Hero WHERE hero_name="{}";""".format(hero_name))
        ID = int(cursor.fetchone()[0])
        cursor.execute("""DELETE FROM Hero WHERE hero_name="{}";""".format(hero_name))
        cursor.execute("""DELETE FROM Hero_stats WHERE hero_number={};""".format(ID))

        connection.commit()
        connection.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main_UI()
    sys.exit(app.exec_())