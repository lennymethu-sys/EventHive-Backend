from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/users', methods=['GET'])
@jwt_required()
def get_all_users():
    from models.models import User
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    users = User.query.all()
    return jsonify([{
        'id': u.id,
        'username': u.username,
        'email': u.email,
        'role': u.role
    } for u in users]), 200

@admin_bp.route('/admin/users/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    from extensions import db
    from models.models import User
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200
