from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/categories', methods=['GET'])
def get_categories():
    from models.models import Category
    categories = Category.query.all()
    return jsonify([{'id': c.id, 'name': c.name, 'description': c.description, 'icon': c.icon, 'color': c.color} for c in categories]), 200

@categories_bp.route('/categories', methods=['POST'])
@jwt_required()
def create_category():
    from extensions import db
    from models.models import Category
    data = request.get_json()
    category = Category(name=data['name'], description=data.get('description', ''), icon=data.get('icon', ''), color=data.get('color', '#e94560'))
    db.session.add(category)
    db.session.commit()
    return jsonify({'id': category.id, 'name': category.name}), 201
