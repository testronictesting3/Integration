from app.webhooks import webhook
from flask import render_template, Flask

@webhook.route('/', methods=['GET'])
def index():
    return render_template("webhooks/home.html")
