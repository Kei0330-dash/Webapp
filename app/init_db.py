import sqlite3

DATABASE = "database.db"

def initialize_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # threads テーブルを作成
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS threads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL
        )
    ''')

    # posts テーブルを作成
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            thread_id INTEGER,
            content TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (thread_id) REFERENCES threads (id)
        )
    ''')

    conn.commit()
    conn.close()
    print("データベースが初期化されました。")

if __name__ == "__main__":
    initialize_database()
