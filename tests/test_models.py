# Local modules
from app.models import User, Event
from app.extensions import bcrypt

# External modules
import unittest
from datetime import datetime

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

    def test_new_admin(self):
        """
        GIVEN a User model
        WHEN a new User is created
        THEN check the email, hashed_password, and role fields are defined correctly
        """
        user = User(name='patkennedy', email='patkennedy79@gmail.com', password=bcrypt.generate_password_hash("FlaskIsAwesome"), role='admin')
        assert user.name == 'patkennedy'
        assert user.email == 'patkennedy79@gmail.com'
        assert user.password != 'FlaskIsAwesome'
        assert user.role == 'admin'

class TestEvent(unittest.TestCase):
    def test_new_event(self):
        """
        GIVEN a Event model
        WHEN a new Event is created
        THEN check the title, description, datetime, and created_by fields are defined correctly
        """
        new_event = Event(title='testing', description='testing', date=datetime(2050,12,12,10,10), created_by='patkennedy')
        assert new_event.title == 'testing'
        assert new_event.description == 'testing'
        # TODO: Fix this, how does SQL store this in table?
        #assert new_event.datetime == datetime(2050,12,12,10,10)
        assert new_event.created_by == 'patkennedy'
