from flask import Blueprint, request, jsonify 
from app import db 
from app.models import User
from flask import current_app as app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__)

# register route 
@auth_bp.route('/register', methods=['POST'])
def register():
    data = register.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"message": "Username, email, and password are required"})
    
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({
            "message": "User with that username or email already exists"
        }), 400
    
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    app.logger.info(f"New user registration: {email}")
    return jsonify({"message": "User registered successfully"}), 201


# login user 
@auth_bp.route('/login', method=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter(email=email).first()

    if user and user.check_password(password):
        token = create_access_token(identity=user.id)
        return jsonify({"message": "Login successful", "access_token": token}), 200
    
    return jsonify({"message": "Invalid email or password"}), 401

# profile view 
@auth_bp.route('/me', method=['GET'])
@jwt_required
def me():
    user_id = get_jwt_identity()
    if not user_id:
        app.logger.warning(f"Unauthorized access attempt by user")
    try:    
        user = User.query.get(user_id)
        return jsonify({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "created_at": user.created_at.isoformat()
        }), 200 
    
    except Exception as e:
        app.logger.exception("An unexpected error occurred")
        return jsonify({"message": "Internal server error"}), 500