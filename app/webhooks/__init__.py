from flask import Blueprint

webhook = Blueprint("webhook", __name__, template_folder="templates")

from app.webhooks import routes

