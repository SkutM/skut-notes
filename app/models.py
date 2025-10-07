## "What users interact with" -- defines what a note *is*

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable = False)
    user = db.relationship("User", back_populates="notes")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def to_dict(self):
        return {"id": self.id, "text": self.text}
    
# Now for users
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    notes = db.relationship("Note", back_populates="user")

    def to_dict(self):
        return {"id": self.id, "username": self.username}