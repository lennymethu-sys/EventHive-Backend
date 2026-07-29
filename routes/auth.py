from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    from extensions import db, bcrypt
    from models.models import User
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    hashed = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(username=data['username'], email=data['email'], password_hash=hashed, role=data.get('role', 'attendee'))
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    from extensions import bcrypt
    from models.models import User
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    token = create_access_token(identity=str(user.id))
    return jsonify({'token': token, 'user': {'id': user.id, 'username': user.username, 'email': user.email, 'role': user.role}}), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    from models.models import User
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email, 'role': user.role}), 200
