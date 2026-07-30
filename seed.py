from app import app
from extensions import db, bcrypt
from models.models import User, Event, Category

with app.app_context():
    db.create_all()

    # Only seed if empty
    if User.query.count() == 0:
        admin = User(
            username='admin',
            email='admin@eventhive.com',
            password_hash=bcrypt.generate_password_hash('admin123').decode('utf-8'),
            role='admin'
        )
        organizer = User(
            username='Lucky',
            email='lucky@eventhive.com',
            password_hash=bcrypt.generate_password_hash('password123').decode('utf-8'),
            role='organizer'
        )
        db.session.add_all([admin, organizer])
        db.session.commit()

    if Category.query.count() == 0:
        categories = [
            Category(name='Tech', description='Technology events', icon='💻', color='#4299e1'),
            Category(name='Music', description='Music events', icon='🎵', color='#e94560'),
            Category(name='Sports', description='Sports events', icon='⚽', color='#48bb78'),
            Category(name='Food', description='Food and drink events', icon='🍕', color='#ed8936'),
        ]
        db.session.add_all(categories)
        db.session.commit()

    if Event.query.count() == 0:
        organizer = User.query.filter_by(email='lucky@eventhive.com').first()
        events = [
            Event(title='Nairobi Tech Meetup', description='Monthly tech meetup for developers in Nairobi.', date='2026-08-15', location='iHub, Nairobi', capacity=100, organizer_id=organizer.id, category_id=1),
            Event(title='Afrobeats Night', description='A night of great African music and vibes.', date='2026-08-20', location='Westlands, Nairobi', capacity=200, organizer_id=organizer.id, category_id=2),
            Event(title='Nairobi Marathon', description='Annual city marathon through Nairobi CBD.', date='2026-09-01', location='Uhuru Park, Nairobi', capacity=500, organizer_id=organizer.id, category_id=3),
            Event(title='Food Festival Nairobi', description='Taste cuisines from all over Kenya and beyond.', date='2026-09-10', location='Carnivore Grounds, Nairobi', capacity=300, organizer_id=organizer.id, category_id=4),
        ]
        db.session.add_all(events)
        db.session.commit()
        print('Database seeded successfully!')
    else:
        print('Database already has data.')
