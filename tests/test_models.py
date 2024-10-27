import unittest
from app.models import User
from app.extensions import bcrypt

class TestNewUser(unittest.TestCase):

# from https://testdriven.io/blog/flask-pytest/
    def test_new_volunteer(self):
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

    def test_new_org(self):
        """
        GIVEN a User model
        WHEN a new User is created
        THEN check the email, hashed_password, and role fields are defined correctly
        """
        user = User(name='patkennedy', email='patkennedy79@gmail.com', password=bcrypt.generate_password_hash("FlaskIsAwesome"),
            role='organization')
        assert user.name == 'patkennedy'
        assert user.email == 'patkennedy79@gmail.com'
        assert user.password != 'FlaskIsAwesome'
        assert user.role == 'organization'
