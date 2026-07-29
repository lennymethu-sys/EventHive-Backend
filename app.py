from flask import Flask
from flask_cors import CORS
from extensions import db, migrate, jwt, bcrypt

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eventhive.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'eventhive-secret-key'

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    CORS(app)

    from models.models import User, Event, Category, Ticket
    from routes.auth import auth_bp
    from routes.events import events_bp
    from routes.tickets import tickets_bp
    from routes.categories import categories_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(tickets_bp)
    app.register_blueprint(categories_bp)

    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
