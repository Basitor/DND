import sqlite3
connection = sqlite3.connect("company.db")

cursor = connection.cursor()


# delete
cursor.execute("""DROP TABLE Hero;""")
cursor.execute("""DROP TABLE Item;""")

# Hero table
sql_command = """
CREATE TABLE Hero (
hero_number INTEGER PRIMARY KEY,
hero_name VARCHAR(20));"""

cursor.execute(sql_command)

# Item table
sql_command_2 = """
CREATE TABLE Item ( 
item_number INTEGER PRIMARY KEY,
item_name VARCHAR(20), 
item_descr VARCHAR(70), 
STR INT(2),
AGI INT(2),
MAGIC INT(2),
hero_number INT(2));"""

cursor.execute(sql_command_2)
