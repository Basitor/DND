import sqlite3
connection = sqlite3.connect("company.db")

cursor = connection.cursor()


# delete
cursor.execute("""DROP TABLE Hero;""")
cursor.execute("""DROP TABLE Item;""")
cursor.execute("""DROP TABLE Hero_stats;""")

# Hero table
sql_command = """
CREATE TABLE Hero (
hero_number INTEGER PRIMARY KEY,
hero_name VARCHAR(20),
hero_level INT(2),
hero_class VARCHAR(20),
hero_story VARCHAR(20),
hero_race VARCHAR(20),
hero_ideology VARCHAR(20),
hero_experience INT(10),
player_name VARCHAR(20));"""

cursor.execute(sql_command)

# Item table
sql_command = """
CREATE TABLE Item ( 
item_number INTEGER PRIMARY KEY,
item_name VARCHAR(20), 
item_descr VARCHAR(70), 
STR INT(2),
AGI INT(2),
MAGIC INT(2),
hero_number INT(2));"""

cursor.execute(sql_command)

# Hero stats table
sql_command = """
CREATE TABLE Hero_stats (
hero_number INTEGER PRIMARY KEY,
STR INT(2),
AGI INT(2),
CONSTITUTION INT(2),
INT INT(2),
WISDOM INT(2),
CHAR INT(2));"""

cursor.execute(sql_command)
connection.close()

