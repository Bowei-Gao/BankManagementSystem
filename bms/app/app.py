from flask import Flask
from app.config import Config
from app.views import register_app
from app.config import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_app(app)
    db.init_app(app)
    return app
