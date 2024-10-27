from app.models import User
from app.extensions import bcrypt

# from https://testdriven.io/blog/flask-pytest/
def test_nologin_redirects(test_client):
    """
    GIVEN a Flask application configured for testing and a user is not logged in
    WHEN any page requiring a user to be logged in is requested (GET)
    THEN check that the response redirects to the login page.
    """
    response = test_client.get('/') # home page
    assert response.status_code == 302
    response = test_client.get('/rewards')
    assert response.status_code == 302
    response = test_client.get('/edit_profile')
    assert response.status_code == 302
    response = test_client.get('/add_hours')
    assert response.status_code == 302
    response = test_client.get('/remove_user')
    assert response.status_code == 302
    response = test_client.get('/view_database')
    assert response.status_code == 302
    response = test_client.get('/logout')
    assert response.status_code == 302

# https://blog.miguelgrinberg.com/post/how-to-write-unit-tests-in-python-part-3-web-applications
def test_registration_form(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the /register page is requested (GET)
    THEN check that the response is given and the registration form is given.
    """
    response = test_client.get('/register')
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    # make sure all the fields are included
    assert 'name="name"' in html
    assert 'name="email"' in html
    assert 'name="password"' in html
    assert 'name="confirm_password"' in html
    assert 'name="role"' in html
    assert 'name="submit"' in html

def test_login_form(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the /login page is requested (GET)
    THEN check that the response is given and the login form is given.
    """
    response = test_client.get('/login')
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert 'name="email"' in html
    assert 'name="password"' in html
    assert 'name="submit"' in html

# TODO: NEED HELP
def test_register_user(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN a user correctly fills out registration form (POST)
    THEN check that the form submission is successful and redirects to the home page.
        """
    response = test_client.post('/register', data={
        'name': 'alice',
        'email': 'alice@example.com',
        'password': 'foo',
        'confirm_password': 'foo',
        'role': 'Admin' # How to input this since this is a select, not a field
        # Also the above return 400, should we write an exception for this?
        },
        follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/'
        #
        # # login with new user
        # response = self.client.post('/auth/login', data={
        #     'username': 'alice',
        #     'password': 'foo',
        # }, follow_redirects=True)
        # assert response.status_code == 200
        # html = response.get_data(as_text=True)
        # assert 'Hi, alice!' in html

# NEED HELP. Sends 400 error
def test_login_redirects(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN a user correctly fills out registration form (POST)
    THEN check that the form submission is successful and redirects to the home page.
    """
    User(name='alice',email='alice@example.com',password="foo")
    response = test_client.post('/login', data=dict(email='alice@example.com',password="foo"),follow_redirects=True
        )
    assert response.status_code == 200
    assert response.request.path == '/'
    response = test_client.get('/login')
    assert response.status_code == 302
    response = test_client.get('/register')
    assert response.status_code == 302