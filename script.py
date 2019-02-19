#!/usr/bin/env python3

import os
import configparser
import sqlite3


# read needed fields from file by sections
with open('NEEDED FIELDS.txt') as f:
    data = f.read().strip().split('\n')

fields = dict()
for i in range(len(data)):
    if data[i].startswith('['):
        section = data[i][1:-1]
        fields.setdefault(section, list())

        for val in range(i + 1, len(data)):
            if data[val].startswith('['):
                i = val - 1
                break
            fields[section].append(data[val])

# connect to database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

if not os.path.isdir(os.getcwd() + '/data'):
    print("Please create 'data' subdir and put INI files there")
    exit()

for filename in os.listdir(os.getcwd() + '/data'):
    filename = 'data/' + filename
    # convert files from cp1251 to utf-8 encoding
    try:
        with open(filename, "rb") as sourceFileBin:
            contents = sourceFileBin.read().decode('cp1251')

        with open(filename, "wb") as targetFile:
            targetFile.write(contents.encode("utf-8"))
    except UnicodeDecodeError:
        pass

    # read data from ini-file
    try:
        config = configparser.RawConfigParser(delimiters=('=',), allow_no_value=True, strict=False)
        config.read(filename)
    except configparser.MissingSectionHeaderError:
        continue
    except configparser.ParsingError:
        print("error parsing {}, skipping".format(filename))
    except UnicodeDecodeError:
        print("failed reading {}, skipping".format(filename))

    # form result list
    result = list()
    try:
        result.append(int(cursor.execute("SELECT MAX(id) FROM fields").fetchone()[0]) + 1)
    except TypeError:
        result.append(1)

    for key, values in fields.items():
        for field in values:
            try:
                v = config[key][field]
                result.append(v)
            except KeyError:
                result.append(None)

    # fill database
    question_marks = ','.join(['?'] * (sum(len(v) for _, v in fields.items()) + 1))
    if not cursor.execute("SELECT MAC_Addr FROM fields WHERE MAC_Addr=?", (result[1],)).fetchone():
        cursor.execute("INSERT INTO fields VALUES ({})".format(question_marks), result)
    else:
        usernames = cursor.execute("SELECT Current_User_Name FROM fields WHERE MAC_Addr=?",
                                   (result[1],)).fetchall()[0][0]
        usernames_list = usernames.split('|')
        if result[2] not in usernames_list:
            usernames_new = usernames + '|' + result[2]
            cursor.execute("UPDATE fields SET Current_User_Name = ? WHERE MAC_Addr=?", (usernames_new, result[1]))

conn.commit()
conn.close()
