import sqlite3

DATABASE = 'database.db'

conn = sqlite3.connect(DATABASE)
conn.execute('CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, content TEXT)')
conn.close()
