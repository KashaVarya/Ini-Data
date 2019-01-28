# Ini-Data
Script for saving needed fields from ini-files to database
This script adapted for Window`s computer settings.

_First step:_

Run create_database.py to create a new database with needed fields. If you had old database with name 'database.db' it will rename to 'old_database.db'. AND if you had file 'old_database.db' it will be rewrite!

_Second step:_

Put all your .ini files in folder with name 'data'.

_Third step:_

Create a file with name 'NEEDED FIELDS.txt' that consists of names of sections ([Section]) and names of fields (Mac_Addr). For example:

`[Info]

MAC_Addr

Current_User_Name

[Computer]

CPU_Freq_in_MHz

CPU.BrandName`

_Fourth step:_

Run script.py to fill database by data from all your .ini files. If some files have the same Mac_Addr, then Current_User_Name will be write to one field though '|'.