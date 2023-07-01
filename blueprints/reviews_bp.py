from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import date
from models.user import User
from models.book import Book
from models.review import Review
from init import db
from blueprints.auth_bp import admin_or_owner_required

reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('/add_review', methods=['POST'])
@jwt_required()
def add_review():
    review_data = request.json

    book_id = review_data['book_id']
    book = Book.query.get(book_id)

    user_email = get_jwt_identity()
    stmt = db.select(User).filter_by(email=user_email)
    user = db.session.scalar(stmt)

    new_review = Review(
        review_content=review_data['review_content'],
        date_created=date.today(),
        username=user.username,
        book_id=review_data['book_id'],
        user_id=user.id,
        title=book.title
    )

    book = Book.query.get(review_data['book_id'])
    user.reviews.append(new_review)
    book.reviews.append(new_review)

    db.session.add(new_review)
    db.session.commit()

    return jsonify(message='Review added successfully'), 201


@reviews_bp.route('/update_review', methods=['PUT'])
@jwt_required()
def update_review():
    review_id = int(request.json['review_id'])
    review = Review.query.filter_by(review_id=review_id).first()
    if review:
        admin_or_owner_required(review.user.email)
        review.review_content=request.json['review_content'],
        review.date_created=request.json['date_created'],
        review.username=request.json['username'],
        review.book_id=int(request.json['book_id']),
        review.user_id=int(request.json['user_id']),
        review.title=request.json['title']
        db.session.commit()
        return jsonify(message="You updated a review!"), 202
    else:
        return jsonify(message="Review does not exist"), 404

    
@reviews_bp.route('/delete_review/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id: int):
    review = Review.query.filter_by(review_id=review_id).first()
    if review:
        admin_or_owner_required(review.user.email)
        db.session.delete(review)
        db.session.commit()
        return jsonify(message="You deleted a review"), 202
    else: 
         return jsonify(message="That review does not exist"), 202