from app import app
from flask import render_template, request, jsonify, redirect, url_for, send_from_directory
from app.models import get_all_threads, get_thread_by_id, create_new_thread, sanitize_and_convert_markdown
import sqlite3
import os
from datetime import datetime

DATABASE = "database.db"

@app.route('/')
def index():
	# スレッド一覧をデータベースから取得
	threads = get_all_threads()
	return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_post():
    thread_id = request.form['thread_id']
    content = request.form['content']
    sanitized_content = sanitize_and_convert_markdown(content)
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # 現在のスレッド内の最大 internal_id を取得
    cursor.execute('SELECT MAX(internal_id) FROM posts WHERE thread_id = ?', (thread_id,))
    max_internal_id = cursor.fetchone()[0]
    if max_internal_id is None:
        max_internal_id = 0
    new_internal_id = max_internal_id + 1
    
    # 新しい投稿を追加
    cursor.execute("INSERT INTO posts (thread_id, internal_id, content, timestamp) VALUES (?, ?, ?, datetime('now', 'localtime'))", 
                   (thread_id, new_internal_id, sanitized_content))
    conn.commit()
    post_id = cursor.lastrowid
    cursor.execute('SELECT timestamp FROM posts WHERE id = ?', (post_id,))
    timestamp = cursor.fetchone()[0]
    conn.close()
    return jsonify({'result': 'success', 'id': post_id, 'timestamp': timestamp, 'internal_id': new_internal_id})


@app.route('/posts/<int:thread_id>', methods=['GET'])
def get_posts(thread_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT internal_id, content, timestamp FROM posts WHERE thread_id = ?', (thread_id,))
    posts = cursor.fetchall()
    conn.close()
    
    posts_list = [{'internal_id': row[0], 'content': row[1], 'timestamp': row[2]} for row in posts]
    return jsonify(posts_list)


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
    sanitized_content = sanitize_and_convert_markdown(content)
    if not title or not content:
        return jsonify({'result': 'error', 'message': 'Title and content are required'}), 400

    new_thread_id = create_new_thread(title, content)
    thread = {
        'id': new_thread_id,
        'title': title,
        'posts': [{'internal_id': 1, 'content': sanitized_content, 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]
    }
    thread_filename = f'thread{new_thread_id}.html'
    thread_html = render_template('thread_template.html', thread=thread)
    threads_directory = os.path.join(app.root_path, 'templates/threads')
    os.makedirs(threads_directory, exist_ok=True)
    with open(os.path.join(threads_directory, thread_filename), 'w', encoding='utf-8') as file:
        file.write(thread_html)

    return jsonify({'result': 'success', 'id': new_thread_id})

@app.route('/threads', methods=['GET'])
def get_threads():
    threads = get_all_threads()
    return jsonify(threads)

#静的なファイルのルート定義
@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'templates'),
							'favicon.ico', mimetype='image/vnd.microsoft.icon')
