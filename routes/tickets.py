from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import uuid

tickets_bp = Blueprint('tickets', __name__)

@tickets_bp.route('/tickets', methods=['GET'])
@jwt_required()
def get_tickets():
    from extensions import db
    from models.models import Ticket
    user_id = get_jwt_identity()
    tickets = Ticket.query.filter_by(user_id=user_id).all()
    return jsonify([t.to_dict() for t in tickets]), 200

@tickets_bp.route('/tickets', methods=['POST'])
@jwt_required()
def create_ticket():
    from extensions import db
    from models.models import Ticket
    data = request.get_json()
    user_id = get_jwt_identity()
    ticket = Ticket(user_id=user_id, event_id=data['event_id'], ticket_code=str(uuid.uuid4())[:8].upper())
    db.session.add(ticket)
    db.session.commit()
    return jsonify(ticket.to_dict()), 201

@tickets_bp.route('/tickets/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_ticket(id):
    from extensions import db
    from models.models import Ticket
    ticket = Ticket.query.get(id)
    if not ticket:
        return jsonify({'error': 'Ticket not found'}), 404
    db.session.delete(ticket)
    db.session.commit()
    return jsonify({'message': 'Ticket cancelled'}), 200
