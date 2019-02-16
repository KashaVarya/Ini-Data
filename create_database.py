#!/usr/bin/env python3

import os
import sqlite3
from glob import glob


dbfiles = sorted(glob(os.getcwd() + '/database.db*'), reverse=True)
for i in range(0, len(dbfiles)):
    num = len(dbfiles) - i
    os.rename(dbfiles[i], 'database.db.{}'.format(num))

# read needed fields from file
with open('NEEDED FIELDS.txt') as f:
    data = f.read().strip().split('\n')
    fields = [field for field in data if not field.startswith('[')]

# connect to database and create table with needed fields
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute("CREATE TABLE fields (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT)")

for field in fields:
    cursor.execute("ALTER TABLE fields ADD COLUMN '%s' TEXT;" % field)

conn.commit()
conn.close()
