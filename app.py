from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow, fields
from marshmallow import fields
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import timedelta, date
from collections import OrderedDict
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from os import environ
from models.user import User, UserSchema
from models.book import Book, BookSchema
from models.comment import Comment, CommentSchema
from models.review import Review, ReviewSchema
from init import db, ma, bcrypt, jwt

from blueprints.cli_bp import cli_bp
from blueprints.auth_bp import auth_bp
from blueprints.books_bp import books_bp
from blueprints.comments_bp import comments_bp
from blueprints.reviews_bp import reviews_bp

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('DB_URI')
    app.config['JWT_SECRET_KEY'] = environ.get('JWT_KEY')

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(cli_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(comments_bp)
    app.register_blueprint(reviews_bp)

    return app

