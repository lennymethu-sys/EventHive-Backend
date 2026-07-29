from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

events_bp = Blueprint('events', __name__)

@events_bp.route('/events', methods=['GET'])
def get_events():
    from extensions import db
    from models.models import Event
    events = Event.query.all()
    return jsonify([e.to_dict() for e in events]), 200

@events_bp.route('/events/<int:id>', methods=['GET'])
def get_event(id):
    from models.models import Event
    event = Event.query.get(id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404
    return jsonify(event.to_dict()), 200

@events_bp.route('/events', methods=['POST'])
@jwt_required()
def create_event():
    from extensions import db
    from models.models import Event
    data = request.get_json()
    user_id = get_jwt_identity()
    event = Event(title=data['title'], description=data.get('description', ''), date=data['date'], location=data['location'], capacity=data.get('capacity', 100), organizer_id=user_id, category_id=data.get('category_id'))
    db.session.add(event)
    db.session.commit()
    return jsonify(event.to_dict()), 201

@events_bp.route('/events/<int:id>', methods=['PUT'])
@jwt_required()
def update_event(id):
    from extensions import db
    from models.models import Event
    event = Event.query.get(id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404
    data = request.get_json()
    event.title = data.get('title', event.title)
    event.description = data.get('description', event.description)
    event.date = data.get('date', event.date)
    event.location = data.get('location', event.location)
    event.capacity = data.get('capacity', event.capacity)
    db.session.commit()
    return jsonify(event.to_dict()), 200

@events_bp.route('/events/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_event(id):
    from extensions import db
    from models.models import Event
    event = Event.query.get(id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404
    db.session.delete(event)
    db.session.commit()
    return jsonify({'message': 'Event deleted'}), 200
