from app.forms import RegistrationForm
from app.models import User
from flask_wtf import FlaskForm
from wtforms import ValidationError
from app.extensions import bcrypt
import email_validator
import json

def test_nologin_redirects(client):
    """
    GIVEN a Flask application configured for testing and a user is not logged in
    WHEN any page requiring a user to be logged in is requested (GET)
    THEN check that the response redirects to the login page.
    """
    response = client.get('/') # home page
    assert response.status_code == 302
    response = client.get('/rewards')
    assert response.status_code == 302
    response = client.get('/edit_profile')
    assert response.status_code == 302
    response = client.get('/add_hours')
    assert response.status_code == 302
    response = client.get('/remove_user')
    assert response.status_code == 302
    response = client.get('/view_database')
    assert response.status_code == 302
    response = client.get('/logout')
    assert response.status_code == 302

# https://blog.miguelgrinberg.com/post/how-to-write-unit-tests-in-python-part-3-web-applications
def test_register_form(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the /register page is requested (GET)
    THEN check that the response is given and the registration form is given.
    """
    response = client.get('/register')
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    # make sure all the fields are included
    assert 'name="name"' in html
    assert 'name="email"' in html
    assert 'name="password"' in html
    assert 'name="confirm_password"' in html
    assert 'name="role"' in html
    assert 'name="submit"' in html

def test_login_form(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the /login page is requested (GET)
    THEN check that the response is given and the login form is given.
    """
    response = client.get('/login')
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert 'name="email"' in html
    assert 'name="password"' in html
    assert 'name="submit"' in html