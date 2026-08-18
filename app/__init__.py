from flask import Flask
from app.routes import books_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(books_bp)
    return app