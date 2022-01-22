from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

app = Flask(__name__)
try:
    db_host = os.environ['POSTGRES_HOST']
    db_port = os.environ['POSTGRES_PORT']
    db_user = os.environ['POSTGRES_USER']
    db_password = os.environ['POSTGRES_PASSWORD']
    db_name = os.environ['POSTGRES_DB']

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}'
except KeyError:
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:pass@localhost/blog_db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'test_cism_2022'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'

from blog import routes
