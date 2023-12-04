from flask import Blueprint, render_template, Flask

board = Blueprint("board", __name__, template_folder="templates")

from app.boards import routes
