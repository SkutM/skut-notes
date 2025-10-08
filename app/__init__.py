## "Where it all connects" -- creates the app and ties routes +
## database together

from flask import Flask
# imports db object we created in models.py
from app.models import db
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from datetime import timedelta

def create_app():
    app = Flask(__name__) # flask application object

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notes.db"
    # performance setting -- don't track every db change in memory
    # i.e., think of it as "turning off extra logging"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "super-secret-key"

    # new config for tokens
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)

    jwt = JWTManager(app)

    # plugs db engine into Flask app
    # "Here's the Flask app to work with. Use its configuration
    # (like the URI above) whenever you create or query data"
    db.init_app(app)
    # new for tokens...?
    jwt.init_app(app)

    # "Use this Flask's app's settings while I run the next few
    # lines."
    with app.app_context():
        # checks all models (like Note) & creates tables for them
        # in the db file (notes.db) *if they don't exist yet*
        db.create_all() # ensures tables from models.py exist

    @app.get("/") # when someone sends a GET request to path /
                  # run the function below (when http:// called)
    def root():
        return {"message": "Hello from Cloud Notes!"}
    
    from app.routes.notes import notes_bp # if defined earlier,
    
    #now import from auth
    from app.routes.auth import auth_bp
    app.register_blueprint(notes_bp)
    # new for auth
    app.register_blueprint(auth_bp)

    return app