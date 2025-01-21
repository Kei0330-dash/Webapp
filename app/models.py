import sqlite3

DATABASE = "database.db"

def get_all_threads():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM threads")
    threads = cursor.fetchall()
    conn.close()
    return [{'id': row[0], 'title': row[1]} for row in threads]

def get_thread_by_id(thread_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM threads WHERE id = ?", (thread_id,))
    thread = cursor.fetchone()
    cursor.execute("SELECT id, content, timestamp FROM posts WHERE thread_id = ?", (thread_id,))
    posts = cursor.fetchall()
    conn.close()
    return {'id': thread[0], 'title': thread[1], 'posts': [{'id': row[0], 'content': row[1], 'timestamp': row[2]} for row in posts]}

def create_new_thread(title, content):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # スレッドを作成
    cursor.execute("INSERT INTO threads (title) VALUES (?)", (title,))
    thread_id = cursor.lastrowid
    
    # 新規スレッドの最初の投稿にinternal_idを設定
    cursor.execute("INSERT INTO posts (thread_id, internal_id, content, timestamp) VALUES (?, ?, ?, datetime('now', 'localtime'))", 
                   (thread_id, 1, content))
    conn.commit()
    conn.close()
    return thread_id

