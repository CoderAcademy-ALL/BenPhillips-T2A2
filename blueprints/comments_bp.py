from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import date
from models.user import User
from models.comment import Comment
from init import db
from blueprints.auth_bp import admin_or_owner_required

comments_bp = Blueprint('comments', __name__)

@comments_bp.route("/add_comment", methods=["POST"])
@jwt_required()
def create_comment():
    
    comment_data = request.json

    comment_content = comment_data.get('comment_content')
    review_id = comment_data.get('review_id')

    user_email = get_jwt_identity()
    stmt = db.select(User).filter_by(email=user_email)
    user = db.session.scalar(stmt)

    new_comment = Comment(
        comment_content=comment_content,
        username=user.username,
        user_id=user.id,
        review_id=review_id,
        date_created=date.today()
    )

    db.session.add(new_comment)
    db.session.commit()
    return jsonify({'message': 'Comment created successfully'})


@comments_bp.route("/delete_comment/<comment_id>", methods=["DELETE"])
@jwt_required()
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)

    if comment:
        admin_or_owner_required(comment.user.email)
        db.session.delete(comment)
        db.session.commit()

        return jsonify({'message': 'Comment deleted successfully'})
    else:
        return jsonify({'message': 'Comment not found'})
    
@comments_bp.route("/edit_comment/<comment_id>", methods=["PUT"])
@jwt_required()
def edit_comment(comment_id):
    comment = Comment.query.get(comment_id)

    if comment:
        admin_or_owner_required(comment.user.email)
        data = request.get_json()
        
        comment.comment_content = data.get('comment_content')

        db.session.commit()

        return jsonify({'message': 'Comment updated successfully'})
    else:
        return jsonify({'message': 'Comment not found'})