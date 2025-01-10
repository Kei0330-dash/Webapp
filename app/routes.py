from app import app
from flask import render_template, request, jsonify, redirect, url_for, send_from_directory
from app.models import get_all_threads, get_thread_by_id, create_new_thread
import sqlite3
import os
DATABASE = "database.db"

@app.route('/')
def index():
    # スレッド一覧をデータベースから取得
    threads = get_all_threads()
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'templates'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/add', methods=['POST'])
def add_post():
    content = request.form['content']
    # データベース操作
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

@app.route('/thread/<int:thread_id>')
def thread(thread_id):
    # 特定のスレッドをデータベースから取得
    thread = get_thread_by_id(thread_id)
    return render_template('threads/thread.html', thread=thread)

@app.route('/create_thread', methods=['POST'])
def create_thread():
    print(request.form)  # フォームデータを出力して確認
    title = request.form.get('title')
    content = request.form.get('content')
    if not title or not content:
        return "タイトルと内容は必須です", 400
    # 新しいスレッドをデータベースに追加
    new_thread_id = create_new_thread(title, content)
    return redirect(url_for('index'))
