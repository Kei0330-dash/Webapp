from flask import Blueprint, request, render_template, redirect, url_for, session
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# ダミーデータ（本番環境ではデータベースを使用）
admin_username = 'admin'
admin_password = 'password'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == admin_username and password == admin_password:
            session['logged_in'] = True
            return redirect(url_for('admin.index'))
        else:
            return "ログイン失敗"
    return render_template('admin_login.html')

@admin_bp.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('admin.login'))

@admin_bp.route('/')
@login_required
def index():
    return '''
        <h1>管理者ページ</h1>
        <ul>
            <li><a href="#">ユーザー管理</a></li>
            <li><a href="#">投稿管理</a></li>
            <li><a href="#">設定変更</a></li>
            <li><a href="{}">ログアウト</a></li>
        </ul>
    '''.format(url_for('admin.logout'))
