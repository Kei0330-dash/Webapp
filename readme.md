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

### プロジェクト構造
/project-root<br>
│<br>
├── /app<br>
│   ├── __pycache__/<br>
│   ├── __init__.py<br>
│   ├── init_db.py<br>
│   ├── routes.py  ← スレッド関連のルートをここに追加します<br>
│<br>
├── /static<br>
│   ├── style.css  ← スタイルシートを追加するならここ<br>
│<br>
├── /templates<br>
│   ├── favicon.ico<br>
│   ├── index.css<br>
│   ├── index.html  ← トップページでスレッドの一覧を表示<br>
│   ├── thread_template.html  ← スレッド用のテンプレート<br>
│   ├── threads/    ← スレッドのHTMLファイルを格納するディレクトリを作成<br>
│       ├── thread1.html<br>
│       ├── thread2.html<br>
│       ├── ... 追加のスレッドファイル<br>
│<br>
├── /memo<br>
│   ├── config.py<br>
│<br>
├── database.db  ← スレッドデータを保持<br>
├── readme.md<br>
├── requirements.txt<br>
├── run.py  ← アプリのエントリーポイント<br>

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
