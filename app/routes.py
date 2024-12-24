from app import app
from flask import render_template, request, jsonify

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_post():
    content = request.form['content']
    # データベース操作をここに追加
    return jsonify({'result': 'success'})

@app.route('/posts', methods=['GET'])
def get_posts():
    # データベースから投稿を取得
    return jsonify([])  # 例として空リストを返す
