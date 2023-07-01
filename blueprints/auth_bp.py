from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import create_access_token, get_jwt_identity
from datetime import timedelta

from models.user import User, UserSchema

from init import db, bcrypt

auth_bp = Blueprint('auth', __name__)

def admin_required():
  user_id = get_jwt_identity()
  stmt = db.select(User).filter_by(id=user_id)
  user = db.session.scalar(stmt)
  if not (user and user.is_admin):
    abort(401)

def admin_or_owner_required(owner_email):
    user_email = get_jwt_identity()
    stmt = db.select(User).filter_by(email=user_email)
    user = db.session.scalar(stmt)
    if not (user and (user.is_admin or user_email == owner_email)):
        abort(401, description='You must be an admin or the owner')

@auth_bp.route("/register", methods=['POST'])
def register():
    email = request.form['email']
    test = User.query.filter_by(email=email).first()
    if test: 
        return jsonify(message="that email already exists"), 409
    else:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User(username=username, email=email, password=bcrypt.generate_password_hash(password).decode('utf8'))
        db.session.add(user)
        db.session.commit()
        return UserSchema(exclude=['password']).dump(user), 201
    
@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        stmt = db.select(User).filter_by(email=request.json['email'])
        user = db.session.scalar(stmt)
        if user and bcrypt.check_password_hash(user.password, request.json['password']):
            token = create_access_token(identity=user.email, expires_delta=timedelta(days=1))
            return {'token': token, 'user': UserSchema(exclude=['password']).dump(user)}
        else:
            return {'error': 'Invalid email address or password'}, 401
    except KeyError:
        return {'error': 'Email and password are required'}, 400


