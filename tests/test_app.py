
# from https://testdriven.io/blog/flask-pytest/
def test_required_login_pages(test_client):
    """
    GIVEN a Flask application configured for testing
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
    WHEN the registration page is requested (GET)
    THEN check that the response redirects to the login page.
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
    response = test_client.get('/login')
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert 'name="email"' in html
    assert 'name="password"' in html
    assert 'name="submit"' in html

# TODO: Fix this case
def test_register_user(test_client):
    response = test_client.post('/register', data={
        'username': 'alice',
        'email': 'alice@example.com',
        'password': 'foo',
        'confirm_password': 'foo',
        'role': 'admin', # not a field, select from dropdown
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
# TODO: Test fields in edit profile form. How to do this when login required?
# TODO: Test that logged in users redirect when accessing /register, /login