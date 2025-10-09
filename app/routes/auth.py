from flask import Blueprint
# jwt extended here now, creates signed token
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import jwt_required, get_jwt_identity


# creates new mini "route group" called auth_bp
# prefixes all its routes with /api, so if you define:
# @auth_bp.post("/register")
# the actual route becomes:
# /api/register
auth_bp = Blueprint("auth", __name__, url_prefix="/api")

# avoid circular import
from flask import request, jsonify, abort
from app.models import db, User

@auth_bp.post("/register")
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return {"error": "Username and password are required"}, 400

    # user is either a User object (if exists) or None (if DNE)
    existing_user = User.query.filter_by(username=username).first()

    if existing_user is not None:
        return {"error": f"Username '{username}' already exists"}, 400

    # otherwise, create new user
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return {"message": "User created successfully!"}, 201

@auth_bp.post("/login")
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return {"error": "Username and password are required"}, 400
    
    user = User.query.filter_by(username=username).first()
    if user is None:
        return {"error": f"Username '{username}' does not exist"}, 404

    if not user.check_password(password):
        return {"error": "Invalid password"}, 401
    # db.session.commit() only for data changes

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user_id": user.id
    }, 200

@auth_bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user)
    return {"access_token": new_token}, 200

# 401 = Unauthorized
