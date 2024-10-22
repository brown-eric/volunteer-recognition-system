# Flask modules
from flask_login import UserMixin

# Other modules
from datetime import datetime

# Local modules
from app.extensions import db

class HoursLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hours_added = db.Column(db.Integer, nullable=False)
    added_by = db.Column(db.String(255), nullable=False)  # The name or email of the volunteering organization who added the hours
    added_to = db.Column(db.String(255), nullable=False)  # The email of the user who received the hours
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # When the hours were added

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    hours_volunteered = db.Column(db.Integer, default=0)
    role = db.Column(db.String(80), nullable=False, default='volunteer')



    def __repr__(self):
        return f'<User {self.name}>'


__all__ = [User, ]
