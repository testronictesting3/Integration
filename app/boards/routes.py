from app.boards import board
from flask import Flask, render_template, request, redirect, url_for, jsonify

@board.route("/" , methods=["GET"])
def index():
    return "Board route"

@board.route("/jobRequest", methods=["GET"])
def jobRequest():
    return render_template("job.html")

