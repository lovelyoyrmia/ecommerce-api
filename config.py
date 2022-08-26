import os
from flask import Flask
from model import db


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["SQLALCHEMY_DATABASE_URI"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = "secret string"

    db.init_app(app)

    return app
