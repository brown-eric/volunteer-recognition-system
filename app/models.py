# Flask modules
from flask_login import UserMixin

# Other modules
from datetime import datetime

# Local modules
from app.extensions import db

class HoursLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hours_added = db.Column(db.Integer, nullable=False)
    added_by_email = db.Column(db.String(255), nullable=False) # The email of the volunteering organization who added the hours
    added_by_username = db.Column(db.String(80), nullable=False)  # The username of the volunteering organization who added the hours
    added_to = db.Column(db.String(255), nullable=False)  # The email of the user who received the hours
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # When the hours were added

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.String(80), nullable=False)  # Stores the name or email of the creating organization
    attendees = db.relationship('User', secondary='event_attendees', backref='events')


event_attendees = db.Table('event_attendees',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True)
)

volunteer_organization = db.Table('volunteer_organization',
    db.Column('organization_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('volunteer_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    hours_volunteered = db.Column(db.Integer, default=0)
    role = db.Column(db.String(80), nullable=False, default='volunteer')
    volunteers = db.relationship(
        'User', secondary=volunteer_organization,
        primaryjoin=(volunteer_organization.c.organization_id == id),
        secondaryjoin=(volunteer_organization.c.volunteer_id == id),
        backref=db.backref('organizations', lazy='dynamic'),
        lazy='dynamic'
    )


def __repr__(self):
    return f'<User {self.name}>'


__all__ = [User, ]
