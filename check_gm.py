#!/usr/bin/env python3
# vi:tabstop=4:expandtab:shiftwidth=4:softtabstop=4:autoindent:smarttab

import os, sys
import sqlite3

g_err = False

file_path = 'database/tables.sql'
with open(file_path, 'r', encoding='utf-8') as file:
    schema = file.read()

db = sqlite3.connect(':memory:')
db.executescript(schema)
print('\nTesting reports with MMEX db schema')
print('-' * 40)
valid_names = ['description.txt', 'luacontent.lua', 'sqlcontent.sql', 'template.htt']
path = 'packages'

for subdir, dirs, files in os.walk(path):
    file_count = len(files)    
    if file_count < 4: continue
    error_msg = ''
    err = False
    package = ''
    for filename in files:
        path, subfolder = os.path.split(subdir)
        package = subfolder
        if filename in valid_names:
            if filename == 'sqlcontent.sql':
                try: db.executescript(open(os.path.join(path, subfolder, filename)).read())
                except sqlite3.Error as e:
                    error_msg = '| SQL: ' + e.args[0] + '|'
                    err = g_err = True

                db.rollback()
    for filename in valid_names:
        if not filename in files:
            error_msg = error_msg + ' | file:' + filename + ' is missing '
            err = g_err = True
    if err: print('[X] ', end = "")
    else: print('[V] ', end = "")
    print(package, error_msg)
        
db.close()
if g_err: sys.exit(1)
