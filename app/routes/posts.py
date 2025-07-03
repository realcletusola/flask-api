from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import current_app as app
from app import db 
from app.models import Post, User 

post_bp = Blueprint('posts', __name__)

# Create a new post 
@post_bp.route('/', methods=['POST'])
@jwt_required()
def create_post():
    data = request.get_json()
    title = data.get("title")
    content = data.get("content")

    if not title or not content:
        return jsonify({"message": "Title and content are required"}), 400
    
    user_id = get_jwt_identity()
    post = Post(title=title, content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()

    app.logger.info(f"New post created")
    return jsonify({"message": "Post created successfully", "id":post.id}), 201

# Get all posts 
@post_bp.route('/', methods=['GET'])
@jwt_required()
def get_posts():
    posts = Post.query.all()
    results = []
    for post in posts:
        results.append({
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "author_id": post.user_id,
            "created_at": post.created_at.isoformat()
        })
    return jsonify(results), 200


# Get a single post 
@post_bp.route('/<int:post_id>', methods=['GET'])
@jwt_required()
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify({
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "author_id": post.user_id,
        "created_at": post.created_at.isoformat()
    }), 200 


# Update a post 
@post_bp.route('/<int:post_id>', methods=['POST'])
@jwt_required()
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    user_id = get_jwt_identity

    if post.user_id != user_id:
        app.logger.warning(f"Unauthorized access attempt by user")
        return jsonify({"message": "Unauthorized"}), 403
    
    data = request.get_json()
    post.title = data.get("title", post.title)
    post.content = data.get("content", post.content)

    db.session.commit()
    return jsonify({"message": "Post updated successfully"}), 200

# Delete a post
@post_bp.route('/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    user_id = get_jwt_identity

    if post.user_id != user_id:
        return jsonify({"message": "Unauthorized"}), 403 
    
    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Post deleted"}), 204