from dotenv import load_dotenv
import os

load_dotenv()

class Config(object):
  SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SECRET_KEY = os.environ.get('SECRET')
