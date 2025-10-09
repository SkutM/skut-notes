## "How users interact" -- adds, reads, deletes

from flask import Blueprint, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Note

notes_bp = Blueprint("notes", __name__, url_prefix="/api")

@notes_bp.get("/<int:user_id>/notes")
@jwt_required()
def get_notes(user_id):
    current_user = int(get_jwt_identity())

    if current_user != user_id:
        return {"error": "You are not authorized to view these notes"}, 403

    notes = Note.query.filter_by(user_id=user_id).all()
    return {"notes": [note.to_dict() for note in notes]}

# add_note handles POST /api/notes --> expects JSON like {"test": "Buy milk"}
@notes_bp.post("/<int:user_id>/notes")
@jwt_required()
def create_note(user_id):
    _ensure_owner(user_id)
    data = request.get_json()
    text = data.get("text")

    if not text:
        return {"error": "Missing note text"}, 400

    new_note = Note(text=text, user_id=user_id)
    db.session.add(new_note) # stage for saving
    db.session.commit() # write change to notes.db

    return {"message": "Note added!", "note": new_note.to_dict()}, 201

@notes_bp.put("/<int:user_id>/notes/<int:note_id>")
@jwt_required()
def put_note(user_id, note_id):
    _ensure_owner(user_id)
    data = request.get_json()
    text = data.get("text")

    note = get_note_or_404(user_id, note_id)

    if not text:
        return {"error": "Missing note text"}, 400
    
    note.text = text
    db.session.commit()
    
    return note.to_dict(), 200

@notes_bp.delete("/<int:user_id>/notes/<int:note_id>")
@jwt_required()
def delete_note(user_id, note_id):
    _ensure_owner(user_id)
    note = get_note_or_404(user_id, note_id)
    db.session.delete(note)
    db.session.commit()

    return "", 204

def get_note_or_404(user_id, note_id):
    note = Note.query.filter_by(id=note_id, user_id=user_id).first()
    if note is None:
        return {"error": f"Note {note_id} not found for user {user_id}"}, 403
    return note

# handles jwt ownership
def _ensure_owner(user_id):
    current_user = int(get_jwt_identity())
    if current_user != user_id:
        return {"error": "You are not authorized to modify these notes"}, 403


# 200 --> OK (normal successful response)
# 201 --> Created (when something new was successfully made)
# 204 --> No Content (when deleting successful)
# 404 --> Not Found
# 400 --> Bad Request
# 500 --> Internal Server Error