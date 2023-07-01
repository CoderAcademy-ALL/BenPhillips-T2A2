from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from models.book import Book, BookSchema
from init import db

books_bp = Blueprint('books', __name__)

@books_bp.route("/books", methods=["GET"])
def books():
    stmt = db.select(Book).order_by(Book.book_id.asc())
    books = db.session.scalars(stmt).all()
    return BookSchema(many=True).dump(books)


@books_bp.route('/book_details/<int:book_id>', methods=['GET'])
def book_details(book_id: int):
  stmt = db.select(Book).filter_by(book_id=book_id)
  book = db.session.scalar(stmt)
  if book:
    return BookSchema().dump(book)
  else:
    return {'error': 'Book not found'}, 404
    

@books_bp.route('/add_book', methods=['POST'])
@jwt_required()
def add_book():
    title = request.form['title']
    test = Book.query.filter_by(title=title).first()
    if test:
        return jsonify("There is already a book with that title"), 409
    else:
        genre = request.form['genre']
        author = request.form['author']
        synopsis = request.form['synopsis']
        publication_year = int(request.form['publication_year'])

        new_book = Book(title=title, author=author, genre=genre, synopsis=synopsis, publication_year=publication_year)

        db.session.add(new_book)
        db.session.commit()
        return jsonify(message="You added a new book!"), 201

@books_bp.route('/update_book', methods=['PUT'])
@jwt_required()
def update_book():
    book_id = int(request.form['book_id'])
    book = Book.query.filter_by(book_id=book_id).first()
    if book:
        book.title = request.form['title']
        book.author = request.form['author']
        book.genre = request.form['genre']
        book.synopsis = request.form['synopsis']
        book.publication_year = int(request.form['publication_year'])
        db.session.commit()
        return jsonify(message="You updated a book!"), 202
    else:
        return jsonify(message="Book does not exist"), 404

@books_bp.route('/delete_book/<int:book_id>', methods=['DELETE'])
@jwt_required()
def delete_book(book_id: int):
    book = Book.query.filter_by(book_id=book_id).first()
    if book:
        db.session.delete(book)
        db.session.commit()
        return jsonify(message="You deleted a book"), 202
    else: 
         return jsonify(message="That book does not exist"), 202