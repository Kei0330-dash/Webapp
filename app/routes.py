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
    conn.execute('INSERT INTO posts (content) VALUES (?)', (content,))
    conn.commit()
    conn.close()
    return jsonify({'result': 'success'})

@app.route('/posts', methods=['GET'])
def get_posts():
    # データベースから投稿を取得
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM posts')
    posts = cursor.fetchall()
    conn.close()
    
	# JSON形式に変換
    posts_list = [{'id': row[0], 'content': row[1]} for row in posts]
    return jsonify({posts_list})  # JSON形式で返す
