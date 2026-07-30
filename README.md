# EventHive API

EventHive is a platform for discovering and registering for events in Nairobi. This is the backend — a Flask REST API that handles everything from user authentication to ticket management.

## What it does

- Lets users register and log in securely using JWT tokens
- Lets organizers create and manage events
- Lets attendees browse events and register for them with a unique ticket code
- Keeps events organized by category

## Built with

- Python + Flask
- SQLAlchemy for the database
- JWT for authentication
- Bcrypt for password hashing
- SQLite (local) — easily swappable for PostgreSQL in production

## Getting it running locally

You'll need Python 3.8+ installed.

```bash
git clone https://github.com/lennymethu-sys/EventHive-Backend.git
cd EventHive-Backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

That's it. The API runs on http://localhost:5000.

## API overview

**Authentication**
- `POST /register` — create an account
- `POST /login` — log in and get a token
- `GET /me` — get the currently logged in user (requires token)

**Events**
- `GET /events` — list all events
- `GET /events/<id>` — get a single event
- `POST /events` — create an event (organizers only)
- `PUT /events/<id>` — update an event (organizers only)
- `DELETE /events/<id>` — delete an event (organizers only)

**Tickets**
- `GET /tickets` — see your tickets
- `POST /tickets` — register for an event
- `DELETE /tickets/<id>` — cancel a ticket

**Categories**
- `GET /categories` — list all categories
- `POST /categories` — add a category (admin only)

## Data models

There are four models: **User**, **Event**, **Category**, and **Ticket**.

Users can be attendees, organizers, or admins. Organizers create events. Attendees register for events and get tickets. A ticket is the link between a user and an event — so users and events have a many-to-many relationship through tickets.

## Live API

https://eventhive-backend-production.up.railway.app

## License

MIT
