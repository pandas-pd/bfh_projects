import sqlite3
from sqlite3 import Error 
import os


db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"first_database.db")
print(db_path)
table_name = "first_table"

#connecting to db
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

#creating table
cursor.execute(f"""CREATE TABLE {table_name} (
    id, first_name, last_name
    )""")
connection.commit()

#write new row
cursor.execute (f"""INSERT INTO {table_name} VALUES (0, 'Joel', 'Tauss');""")
cursor.execute (f"""INSERT INTO {table_name} VALUES (1, 'Köbu', 'Marth');""")
connection.commit()

#print table header     )
cursor.execute(f"""PRAGMA table_info({table_name})""")
table_header = cursor.fetchall()
column_names = []
for item in table_header:
    column_names.append(item[1])
print(column_names)

#print table content
cursor.execute(f"""SELECT * FROM {table_name}""")
table_content = cursor.fetchall()
print(table_content)

#delet table
cursor.execute(f"""DROP TABLE {table_name}""")
connection.commit()