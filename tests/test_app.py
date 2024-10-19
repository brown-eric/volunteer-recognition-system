

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