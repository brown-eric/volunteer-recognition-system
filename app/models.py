# Flask modules
from flask_login import UserMixin

# Other modules
from datetime import datetime

# Local modules
from app.extensions import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    #add default role to volunteer
    role = db.Column(db.String(50), nullable=False, default='volunteer')

    def __repr__(self):
        return f'<User {self.name}>'

    #edit role
    def has_role(self, role_name):
        return self.role == role_name

__all__ = [User, ]
