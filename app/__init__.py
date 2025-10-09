## "Where it all connects" -- creates the app and ties routes +
## database together

from flask import Flask, send_from_directory
from app.models import db
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from datetime import timedelta
from pathlib import Path # for getting right dir (see below)
from werkzeug.exceptions import HTTPException
from flask_cors import CORS

def create_app():
    BASE_DIR = Path(__file__).resolve().parent.parent
    app = Flask(__name__, static_folder=str(BASE_DIR / "static")) # flask application object
    CORS(app)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notes.db"
    # performance setting -- don't track every db change in memory
    # i.e., think of it as "turning off extra logging"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "super-secret-key"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)

    jwt = JWTManager(app)

    db.init_app(app)
    jwt.init_app(app)

    # "Use this Flask's app's settings while I run the next few
    # lines."
    with app.app_context():
        db.create_all() # ensures tables from models.py exist
    
    from app.routes.notes import notes_bp
    from app.routes.auth import auth_bp

    app.register_blueprint(notes_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api")

    @app.route("/")
    def serve_index():
        return send_from_directory(app.static_folder, "index.html")

    return app

