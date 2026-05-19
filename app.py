import os

from flask import Flask
from dotenv import load_dotenv

from backend.config import Config
from backend.extensions import bcrypt, db
from backend.routes import bp

load_dotenv()


def create_app():
    app = Flask(
        __name__,
        template_folder="frontend/templates",
        static_folder="frontend/static"
    )

    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(bp)

    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=False)