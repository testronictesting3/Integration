from flask import Flask, render_template
from app.main import main


@main.route("/", methods=['POST'])
def mainRoute():
    return {"Response": "Main Route "}

@main.route("/", methods=["GET"])
def mainTemplate():
    return render_template("base.html")
