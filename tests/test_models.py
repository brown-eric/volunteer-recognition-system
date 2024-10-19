import unittest
from app.models import User
from app.extensions import bcrypt

def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, and role fields are defined correctly
    """
    user = User(name='patkennedy', email='patkennedy79@gmail.com', password=bcrypt.generate_password_hash("FlaskIsAwesome"), role='volunteer')
    assert user.name == 'patkennedy'
    assert user.email == 'patkennedy79@gmail.com'
    assert user.password != 'FlaskIsAwesome'
    assert user.role == 'volunteer'