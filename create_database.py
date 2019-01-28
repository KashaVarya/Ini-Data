import os
import sqlite3

# if 'database.db' file exists, rename it
if os.path.isfile('./database.db'):
    os.rename('database.db', 'old_database.db')

# create new 'database.db' file
database = open('database.db', 'w+')
database.close()

# read needed fields from file
data = open('NEEDED FIELDS.txt').read().strip().split('\n')
fields = [field for field in data if not field.startswith('[')]

# connect to database and create table with needed fields
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute("CREATE TABLE fields (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT)")

for field in fields:
    cursor.execute("ALTER TABLE fields ADD COLUMN '%s' TEXT;" % field)

conn.commit()
conn.close()
