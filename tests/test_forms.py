import pytest
from flask import Flask
from app import create_app
from app.forms import RegistrationForm
from app.models import db

def test_registration_form_valid_data(app):
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

def test_registration_form_invalid_email(app):
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

def test_registration_form_password_mismatch(app):
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

def test_registration_form_invalid_username(app):
    data = {
        'name': 'invalid username!',
        'email': 'example@ufl.edu',
        'password': 'securePassword123',
        'confirm_password': 'securePassword123',
        'role': 'volunteer'
    }
    with app.test_request_context(), app.test_client() as client:
        form = RegistrationForm(data=data)
        assert not form.validate(), "Form should be invalid with invalid username"
        assert 'Username must contain only letters, numbers, and underscores.' in form.name.errors, "Username field should have invalid characters error"
