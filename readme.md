このプロジェクトは学校の実習用プロジェクトです。<br>
Webアプリの実装実習です。<br>
適宜内容を追加します。

### プロジェクトの進め方
app/staticディレクトリには、cssやjavascriptなどの静的なファイルを入れてください。

### 実行する際の説明
python app/init_db.py　<br>
python run.py <br>
をすれば動きます。多分。<br>
flaskとかsqlite3とかは入れてください。pipすればok

###　プロジェクト構造
/project-root
│
├── /app
│   ├── __pycache__/
│   ├── __init__.py
│   ├── init_db.py
│   ├── routes.py  ← スレッド関連のルートをここに追加します
│
├── /static
│   ├── style.css  ← スタイルシートを追加するならここ
│
├── /templates
│   ├── favicon.ico
│   ├── index.css
│   ├── index.html  ← トップページでスレッドの一覧を表示
│   ├── thread.html  ← スレッド用のテンプレート
│   ├── threads/    ← スレッドのHTMLファイルを格納するディレクトリを作成
│       ├── thread1.html
│       ├── thread2.html
│       ├── ... 追加のスレッドファイル
│
├── /memo
│   ├── config.py
│
├── database.db  ← スレッドデータを保持
├── readme.md
├── requirements.txt
├── run.py  ← アプリのエントリーポイント
### routes.pyの修正
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

@app.route('/')
def index():
    # スレッド一覧をデータベースから取得
    threads = get_all_threads()
    return render_template('index.html', threads=threads)

@app.route('/thread/<int:thread_id>')
def thread(thread_id):
    # 特定のスレッドをデータベースから取得
    thread = get_thread_by_id(thread_id)
    return render_template('threads/thread.html', thread=thread)

@app.route('/create_thread', methods=['POST'])
def create_thread():
    # 新しいスレッドをデータベースに追加
    new_thread = create_new_thread(request.form['title'], request.form['content'])
    return redirect(url_for('index'))
