## "Where it all connects" -- creates the app and ties routes +
## database together

from flask import Flask
# imports db object we created in models.py
from app.models import db

def create_app():
    app = Flask(__name__) # flask application object

    # "Use SQLite, and store the data in a file named notes.db
    # in this project folder."
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notes.db"
    # performance setting -- don't track every db change in memory
    # i.e., think of it as "turning off extra logging"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # plugs db engine into Flask app
    # "Here's the Flask app to work with. Use its configuration
    # (like the URI above) whenever you create or query data"
    db.init_app(app)

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
    
    from app.routes.notes import notes_bp # after flask import -->
                                # first ensure Flask app exists!
    # "Take all the routes defined inside this blueprint & attach
    # them to the main app -- under the URL prefix /api/notes"
    app.register_blueprint(notes_bp)

    return app