import os
from flask import Flask
from config import Config
from app.extensions import database
#import Blueprints
from app.main.routes import main as main_bp
from app.webhooks.routes import webhook as webhook_bp
from app.boards.routes import board as board_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(webhook_bp, url_prefix="/webhooks")
    app.register_blueprint(board_bp, url_prefi="/board")
    return app

app = create_app()
#app = Flask(__name__)
#app.config.from_object(Config)
#app.register_blueprint(main_bp, url_prefix="/")
#app.register_blueprint(webhook_bp, url_prefix="/webhooks")
#app.register_blueprint(board_bp, url_prefix="/board")
#return app

