import sys
import sqlite3
gpt_connection = sqlite3.connect('gpt.db', check_same_thread=False)
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
gpt_connection.row_factory = dict_factory