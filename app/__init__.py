from flask import Flask
from .routes import homeRoutes

app = Flask(__name__)


def init_app():

    # Blueprints
    app.register_blueprint(homeRoutes.main, url_prefix="/")

    return app
