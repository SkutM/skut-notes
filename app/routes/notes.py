## "How users interact" -- adds, reads, deletes

# Blueprint --> defines route section
# request --> gives access to request data (like JSON)
from flask import Blueprint, request, abort
# db & Note --> let us interact w the db
from app.models import db, Note

# create mini Flask app dedicated to /api/notes
notes_bp = Blueprint("notes", __name__, url_prefix="/api/notes")

# get_notes handles GET /api/notes --> returns full list as JSON
@notes_bp.get("/<int:user_id>/notes")
def get_notes(user_id):
    # change to reflect relationships
    notes = Note.query.filter_by(user_id=user_id)
    return {"notes": [note.to_dict() for note in notes]}

# add_note handles POST /api/notes --> expects JSON like {"test": "Buy milk"}
@notes_bp.post("/<int:user_id>/notes")
def create_note(user_id):
    data = request.get_json()
    text = data.get("text")

    if not text:
        return {"error": "Missing note text"}, 400

    new_note = Note(text=text, user_id=user_id)
    db.session.add(new_note) # stage for saving
    db.session.commit() # write change to notes.db

    return {"message": "Note added!", "notes": new_note.to_dict()}, 201

@notes_bp.put("/<int:user_id>/notes/<int:note_id>")
def put_note(user_id, note_id):
    # get current note content
    data = request.get_json()
    text = data.get("text")

    # check if 404 or set note = old note (to be replaced)
    note = get_note_or_404(user_id, note_id)

    if not text:
        return {"error": "Missing note text"}, 400
    
    note.text = text
    db.session.commit()
    
    # update that in dict, 200 = success
    return note.to_dict(), 200


@notes_bp.delete("/<int:user_id>/notes/<int:note_id>")
def delete_note(user_id, note_id):
    # does note exist? if yes, to be deleted
    note = get_note_or_404(user_id, note_id)
    db.session.delete(note)
    db.session.commit()

    return "", 204

def get_note_or_404(user_id, note_id):
    # updated since relationship
    note = Note.query.filter_by(id=note_id, user_id=user_id).first()
    if note is None:
        abort(404, description=f"Note {note_id} not found for user {user_id}")
    return note

# 200 --> OK (normal successful response)
# 201 --> Created (when something new was successfully made)
# 204 --> No Content (when deleting successful)
# 404 --> Not Found
# 400 --> Bad Request
# 500 --> Internal Server Error