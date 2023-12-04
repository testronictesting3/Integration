from flask import Blueprint, render_template, Flask

main = Blueprint("main", __name__, template_folder="templates")

from app.main import routes
