from flask import Flask

app = Flask(__name__)
app.secret_key = 'your_secret_key'

from app import routes
from app.admin import admin_bp

# ブループリントを登録
app.register_blueprint(admin_bp)
