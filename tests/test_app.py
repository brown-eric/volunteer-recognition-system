from app.models import User
from app.extensions import bcrypt
import json

def test_success_registration(client, user_payload):
    """
        GIVEN a Flask application configured for testing
        WHEN a user correctly fills out registration form (POST)
        THEN check that the form submission is successful and redirects to the home page.
    """
    headers = {
        'content-type': 'application/json',
    }
    response = client.post(
        "/register", data=json.dumps(user_payload), content_type="application/json"
    ) # I don't know how to get this to not return 400
    assert response.status_code == 201

    response = client.get("/user/JohnDoe")
    assert response.status_code == 200

    read_response_json = json.loads(response.data)
    print(read_response_json)
    assert len(read_response_json) == 1
# from https://testdriven.io/blog/flask-pytest/
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

# NEED HELP. Sends 400 error
def test_successful_login(client):
    """
    GIVEN a Flask application configured for testing
    WHEN a user correctly fills out login form (POST)
    THEN check that the form submission is successful and redirects to the home page.
    """
    User(name='alice',email='alice@example.com',password="foo", role="volunteer")
    response = client.post('/login', data=dict(email='alice@example.com',password="foo", remember_me=False),follow_redirects=True
        ) # I don't know how to get this to not return 400
    assert response.status_code == 200
    assert response.request.path == '/'
    # response = client.get('/login')
    # assert response.status_code == 302
    # response = client.get('/register')
    # assert response.status_code == 302