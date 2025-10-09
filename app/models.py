## "What users interact with" -- defines what a note *is*

from flask_sqlalchemy import SQLAlchemy
# These two come with Flask (via Werkzeug) & are industry
# standard way to hash and verify passwords
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable = False)
    user = db.relationship("User", back_populates="notes")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def to_dict(self):
        return {"id": self.id, "text": self.text}
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    notes = db.relationship("Note", back_populates="user")
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {"id": self.id, "username": self.username}