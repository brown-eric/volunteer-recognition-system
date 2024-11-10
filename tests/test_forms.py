import pytest
from flask import Flask
from app import create_app
from app.forms import RegistrationForm, LoginForm
from tests.conftest import test_client, init_database
from app.models import db

def test_registration_form_valid_data(app):
    """
    GIVEN a Flask application instance
    WHEN the registration form input is valid
    THEN check if the form is valid
    """
    data = {
        'name': 'validusername',
        'email': 'example@ufl.edu',
        'password': 'securePassword123',
        'confirm_password': 'securePassword123',
        'role': 'volunteer'
    }
    with app.test_request_context(), app.test_client() as client:
        form = RegistrationForm(data=data)
        assert form.validate(), "Form should be valid with correct data"

def test_registration_form_missing_data(app):
    """
    GIVEN a Flask application instance
    WHEN the registration form input is invalid
    THEN check if the form is invalid
    """
    data = {
        'name': '',
        'email': 'example@ufl.edu',
        'password': 'securePassword123',
        'confirm_password': 'securePassword123',
        'role': 'volunteer'
    }
    with app.test_request_context(), app.test_client() as client:
        form = RegistrationForm(data=data)
        assert not form.validate(), "Form should be invalid if username is missing"
        assert 'This field is required.' in form.name.errors, "Username field should have required error"

def test_registration_form_invalid_data(app):
    """
    GIVEN a Flask application instance
    WHEN the registration form input is invalid
    THEN check if the form is invalid
    """
    # Invalid email
    data = {
        'name': 'validusername',
        'email': 'invalid-email',
        'password': 'securePassword123',
        'confirm_password': 'securePassword123',
        'role': 'volunteer'
    }
    with app.test_request_context(), app.test_client() as client:
        form = RegistrationForm(data=data)
        assert not form.validate(), "Form should be invalid with incorrect email format"
        assert 'Invalid email address.' in form.email.errors, "Email field should have invalid email error"

    # Password mismatch
    data = {
        'name': 'validusername',
        'email': 'example@ufl.edu',
        'password': 'securePassword123',
        'confirm_password': 'differentPassword',
        'role': 'volunteer'
    }
    with app.test_request_context(), app.test_client() as client:
        form = RegistrationForm(data=data)
        assert not form.validate(), "Form should be invalid if passwords do not match"
        assert 'Passwords must match' in form.confirm_password.errors, "Confirm Password field should have mismatch error"

    # Invalid username
    data = {
        'name': 'invalid username!',
        'email': 'example@ufl.edu',
        'password': 'securePassword123',
        'confirm_password': 'securePassword123',
        'role': 'volunteer'
    }
    with (app.test_request_context(), app.test_client() as client):
        form = RegistrationForm(data=data)
        assert not form.validate(), "Form should be invalid with invalid username"
        assert 'Username must contain only letters, numbers, and underscores.' in form.name.errors, "Username field should have invalid characters error"

def test_login_form_valid_data(test_client, init_database):
    """
    GIVEN a Flask application instance
    WHEN the login form input is valid
    THEN check if the form is valid
    """
    data = {
        'email': 'testvolunteer@example.com',
        'password': 'password123',
        'remember': False
    }
    form = LoginForm(data=data)
    assert form.validate()

    data = {
        'email': 'testvolunteer@example.com',
        'password': 'password123'
        # remember field should default to False
    }
    form = LoginForm(data=data)
    assert form.validate()

def test_login_form_missing_data(test_client, init_database):
    """
    GIVEN a Flask application instance
    WHEN the login form input is invalid
    THEN check if the form is invalid
    """
    data = {
        'email': '',
        'password': 'password123',
        'remember': False
    }
    form = LoginForm(data=data)
    assert not form.validate(), "Form should be invalid if email is missing"
    assert 'This field is required.' in form.email.errors

    data = {
        'email': 'testvolunteer@example.com',
        'password': ''
    }
    form = LoginForm(data=data)
    assert not form.validate(), "Form should be invalid if password is missing"
    assert 'This field is required.' in form.password.errors

def test_login_form_invalid_data(test_client, init_database):
    """
    GIVEN a Flask application instance
    WHEN the login form input is invalid
    THEN check if the form is invalid

    Note that this only checks if the input in the fields follows the validator constraints,
    not if the email matches a user in the db.
    """
    data = {
        'email': 'testvolunteerexamplecom',
        'password': 'password123'
    }
    form = LoginForm(data=data)
    assert not form.validate(), "Form should be invalid with invalid email"
    assert 'Invalid email address.' in form.email.errors

    data = {
        'email': 'testvolunteer@example.com',
        'password': 'password1234567890123456789012345678901234567890 this is longer than 64 characters which is invalid'
    }
    form = LoginForm(data=data)
    assert not form.validate(), "Form should be invalid with invalid password"
    assert 'Field cannot be longer than 64 characters.' in form.password.errors

def test_edit_profile_form_valid_data(test_client, init_database):
    """
    GIVEN a Flask application instance
    WHEN the edit profile form input is valid
    THEN check if the form is valid
    """

def test_edit_profile_form_invalid_data(test_client, init_database):
    """
    GIVEN a Flask application instance
    WHEN the edit profile form input is invalid
    THEN check if the form is invalid
    """