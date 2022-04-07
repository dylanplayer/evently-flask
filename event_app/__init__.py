from flask import Flask, redirect
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from event_app.config import Config
import os

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.environ.get('SECRET')

db = SQLAlchemy(app)

from event_app.controllers.events import events
from event_app.controllers.users import users

app.register_blueprint(events, url_prefix='/events')
app.register_blueprint(users)

login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.init_app(app)

from event_app.models import User
@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

@app.route('/', methods=['GET'])
def index():
  return(redirect('/events'))

with app.app_context():
  db.create_all()


