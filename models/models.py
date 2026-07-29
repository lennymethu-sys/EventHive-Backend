from datetime import datetime
from extensions import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='attendee')
    profile_picture = db.Column(db.String(255), default='')
    events = db.relationship('Event', backref='organizer', lazy=True)
    tickets = db.relationship('Ticket', backref='user', lazy=True)

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255), default='')
    icon = db.Column(db.String(50), default='')
    color = db.Column(db.String(20), default='#e94560')
    events = db.relationship('Event', backref='category', lazy=True)

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, default='')
    date = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    capacity = db.Column(db.Integer, default=100)
    organizer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    tickets = db.relationship('Ticket', backref='event', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'date': self.date,
            'location': self.location,
            'capacity': self.capacity,
            'organizer_id': self.organizer_id,
            'category_id': self.category_id
        }

class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    status = db.Column(db.String(20), default='confirmed')
    ticket_code = db.Column(db.String(50), unique=True, nullable=False)
    purchased_at = db.Column(db.String(50), default=str(datetime.now()))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'event_id': self.event_id,
            'status': self.status,
            'ticket_code': self.ticket_code,
            'purchased_at': self.purchased_at
        }
