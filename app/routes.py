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
    thread = get_thread_by_id(thread_id)
    if thread is None:
        return render_template('404.html'), 404
    thread_filename = f'thread{thread_id}.html'
    return render_template(f'threads/{thread_filename}', thread=thread)


@app.route('/create_thread', methods=['POST'])
def create_thread():
    title = request.form.get('title')
    content = request.form.get('content')
    if not title or not content:
        return jsonify({'result': 'error', 'message': 'Title and content are required'}), 400

    new_thread_id = create_new_thread(title, content)
    
    # 新スレッドのHTML生成と保存
    thread_filename = f'thread{new_thread_id}.html'
    thread_html = render_template('thread_template.html', title=title, content=content)
    threads_directory = os.path.join(app.root_path, 'templates/threads')
    os.makedirs(threads_directory, exist_ok=True)
    with open(os.path.join(threads_directory, thread_filename), 'w', encoding='utf-8') as file:
        file.write(thread_html)

    return jsonify({'result': 'success', 'id': new_thread_id})



#静的なファイルのルート定義
@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'templates'),
							'favicon.ico', mimetype='image/vnd.microsoft.icon')


