import sqlite3

DATABASE = 'database.db'

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

# `posts` テーブルを削除（存在する場合）
cursor.execute('DROP TABLE IF EXISTS posts')

# `posts` テーブルを新たに作成
cursor.execute("CREATE TABLE posts (id INTEGER PRIMARY KEY, content TEXT, timestamp DATETIME DEFAULT (datetime('now', 'localtime')))")

conn.commit()
conn.close()

# このスクリプトを実行することで、`database.db` ファイルに `posts` テーブルが作成されます。