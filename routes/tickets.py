from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import uuid

tickets_bp = Blueprint('tickets', __name__)

@tickets_bp.route('/tickets', methods=['GET'])
@jwt_required()
def get_tickets():
    from extensions import db
    from models.models import Ticket, Event
    user_id = get_jwt_identity()
    tickets = Ticket.query.filter_by(user_id=user_id).all()
    result = []
    for t in tickets:
        d = t.to_dict()
        event = Event.query.get(t.event_id)
        d['event_title'] = event.title if event else 'Unknown'
        d['event_date'] = event.date if event else ''
        d['event_location'] = event.location if event else ''
        result.append(d)
    return jsonify(result), 200

@tickets_bp.route('/tickets/event/<int:event_id>', methods=['GET'])
@jwt_required()
def get_event_tickets(event_id):
    from models.models import Ticket, User, Event
    user_id = get_jwt_identity()
    event = Event.query.get(event_id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404
    if str(event.organizer_id) != str(user_id):
        return jsonify({'error': 'Unauthorized'}), 403
    tickets = Ticket.query.filter_by(event_id=event_id).all()
    result = []
    for t in tickets:
        user = User.query.get(t.user_id)
        d = t.to_dict()
        d['username'] = user.username if user else 'Unknown'
        d['email'] = user.email if user else ''
        result.append(d)
    return jsonify(result), 200

@tickets_bp.route('/tickets', methods=['POST'])
@jwt_required()
def create_ticket():
    from extensions import db
    from models.models import Ticket
    data = request.get_json()
    user_id = get_jwt_identity()
    existing = Ticket.query.filter_by(user_id=user_id, event_id=data['event_id']).first()
    if existing:
        return jsonify({'error': 'You are already registered for this event'}), 400
    ticket = Ticket(
        user_id=user_id,
        event_id=data['event_id'],
        ticket_code=str(uuid.uuid4())[:8].upper()
    )
    db.session.add(ticket)
    db.session.commit()
    return jsonify(ticket.to_dict()), 201

@tickets_bp.route('/tickets/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_ticket(id):
    from extensions import db
    from models.models import Ticket
    user_id = get_jwt_identity()
    ticket = Ticket.query.get(id)
    if not ticket:
        return jsonify({'error': 'Ticket not found'}), 404
    if str(ticket.user_id) != str(user_id):
        return jsonify({'error': 'Unauthorized'}), 403
    db.session.delete(ticket)
    db.session.commit()
    return jsonify({'message': 'Ticket cancelled'}), 200
