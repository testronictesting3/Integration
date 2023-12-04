import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')\ or 'sqllite:///' + os.path.join(basedir, 'app.db')
    #SQLALCHEMY_TRACK_MODIFICATIONS = False
    MONDAY_URL = os.environ.get('MONDAY_URL')
    MONDAY_API_KEY = os.environ.get('MONDAY_API_KEY')
    XYTECH_URL = os.environ.get('XYTECH_URL')
    XYTECH_UN = os.environ.get('XYTECH_USER')
    XYTECH_PW = os.environ.get('XYTECH_SECRET')

