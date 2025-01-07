from app import app
from flask import render_template, request, jsonify
import sqlite3
DATABASE = "database.db"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_post():
    content = request.form['content']
    # データベース操作をここに追加
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO posts (content, timestamp) VALUES (?, datetime('now', 'localtime'))", (content,))
    conn.commit()
    post_id = cursor.lastrowid
    cursor.execute('SELECT timestamp FROM posts WHERE id = ?', (post_id,))
    timestamp = cursor.fetchone()[0]
    conn.close()
    return jsonify({'result': 'success', 'id': post_id, 'timestamp': timestamp})


@app.route('/posts', methods=['GET'])
def get_posts():
    # データベースから投稿を取得
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM posts')
    posts = cursor.fetchall()
    conn.close()
    
	# JSON形式に変換
    posts_list = [{'id': row[0], 'content': row[1], 'timestamp': row[2]} for row in posts]
    return jsonify(posts_list)  # JSON形式で返す
