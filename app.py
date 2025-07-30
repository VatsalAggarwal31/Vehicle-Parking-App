from flask import Flask
from controllers.database_instance import create_table
from controllers.config import Config
from controllers.database import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    app.app_context().push()

    return app

app = create_app()

from controllers.routes import *

if __name__ == '__main__':

    create_table()
    app.run(debug=True)