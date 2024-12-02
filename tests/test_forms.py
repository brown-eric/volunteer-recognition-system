from app.forms import RegistrationForm, LoginForm, EditProfileForm, AddHoursForm, AddUserForm, RemoveUserForm, CreateEventForm, \
    AddMemberForm
from tests.conftest import test_client, init_database

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

def test_registration_form_invalid_data(test_client, init_database):
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
    #with app.test_request_context(), app.test_client() as client:
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
    # with app.test_request_context(), app.test_client() as client:
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
    #with (app.test_request_context(), app.test_client() as client):
    form = RegistrationForm(data=data)
    assert not form.validate(), "Form should be invalid with invalid username"
    assert 'Username must contain only letters, numbers, and underscores.' in form.name.errors, "Username field should have invalid characters error"

    # Invalid password
    data = {
        'name': 'validusername',
        'email': 'valid@example.com',
        'password': '3p',
        'confirm_password': '3p',
        'role': 'volunteer'
    }
    form = RegistrationForm(data=data)
    assert not form.validate(), "Form should be invalid with invalid password"

    # missing data
    data = {}
    form = RegistrationForm(data=data)
    assert not form.validate(), "Form should be invalid with missing data"
    assert 'This field is required.' in form.name.errors
    assert 'This field is required.' in form.email.errors
    assert 'This field is required.' in form.password.errors
    assert 'This field is required.' in form.confirm_password.errors
    assert 'This field is required.' in form.role.errors

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

    """ missing data """
    data = {}
    form = LoginForm(data=data)
    assert not form.validate(), "Form should be invalid with missing data"
    assert 'This field is required.' in form.email.errors
    assert 'This field is required.' in form.password.errors

def test_edit_profile_form_valid_data(test_client, init_database):
    """
    GIVEN a Flask application instance
    WHEN the edit profile form input is valid
    THEN check if the form is valid
    """
    data = {
        'name': 'testvolunteer',
        'email': 'testvolunteer@example.com'
    }
    form = EditProfileForm(data=data)
    assert form.validate()

def test_edit_profile_form_invalid_data(test_client, init_database):
    """
    GIVEN a Flask application instance
    WHEN the edit profile form input is invalid
    THEN check if the form is invalid
    """
    data = {
        'name': 'testvolunteer!',
        'email': 'testvolunteer@example.com'
    }
    form = EditProfileForm(data=data)
    assert not form.validate(), "Form should be invalid with invalid name"

    data = {
        'name': 'testvolunteer',
        'email': 'testvolunteerexample.com',
    }
    form = EditProfileForm(data=data)
    assert not form.validate(), "Form should be invalid with invalid email"

    # missing data
    data = {}
    form = EditProfileForm(data=data)
    assert not form.validate(), "Form should be invalid with missing data"
    assert 'This field is required.' in form.name.errors
    assert 'This field is required.' in form.email.errors

def test_add_hours_form_valid_data(test_client, init_database):
    """
    GIVEN a Flask application instance
    WHEN the add hours form input is valid
    THEN check if the form is valid
    """
    data = {
        'email': 'testvolunteer@example.com',
        'hours': '10'
    }
    form = AddHoursForm(data=data)
    assert form.validate(), "Form should be valid"

def test_add_hours_form_invalid_data(test_client, init_database):
    """
    GIVEN a Flask application instance
    WHEN the add hours form input is invalid
    THEN check if the form is invalid
    """
    data = {
        'email': 'testvolunteerexample.com',
        'hours': '10'
    }
    form = AddHoursForm(data=data)
    assert not form.validate(), "Form should be invalid with invalid email"

    data = {
        'email': 'testvolunteer@example.com',
        'hours': '10.0'
    }
    form = AddHoursForm(data=data)
    assert not form.validate(), "Form should be invalid with invalid hours"
    data = {
        'email': 'testvolunteer@example.com',
        'hours': '10aa#'
    }
    form = AddHoursForm(data=data)
    assert not form.validate(), "Form should be invalid with invalid hours"
    data = {
        'email': 'testvolunteer@example.com',
        'hours': '0'
    }
    form = AddHoursForm(data=data)
    assert not form.validate(), "Form should be invalid with invalid hours"

    # missing data
    data = {}
    form = AddHoursForm(data=data)
    assert not form.validate(), "Form should be invalid with missing data"
    assert 'This field is required.' in form.email.errors
    assert 'This field is required.' in form.hours.errors

def test_remove_user_form_valid_data(test_client, init_database):
    """
    GIVEN a Flask application instance
    WHEN the remove user form input is valid
    THEN check if the form is valid
    """
    data = {
        'email': 'testvolunteer@example.com'
    }
    form = RemoveUserForm(data=data)
    assert form.validate(), "Form should be valid"

def test_remove_user_form_invalid_data(test_client, init_database):
    """
    GIVEN a Flask application instance
    WHEN the remove user form input is invalid
    THEN check if the form is invalid
    """
    data = {
        'email': 'testvolunteerexample.com'
    }
    form = RemoveUserForm(data=data)
    assert not form.validate(), "Form should be invalid with invalid email"

    # missing data
    data = {}
    form = RemoveUserForm(data=data)
    assert not form.validate(), "Form should be invalid with missing data"
    assert 'This field is required.' in form.email.errors

# TODO:
# def test_add_user_form_valid_data(test_client, init_database):
# def test_add_user_form_invalid_data(test_client, init_database):

def test_create_event_form_valid_data(test_client, init_database):
    """
    GIVEN a Flask application instance
    WHEN the create event form input is valid
    THEN check if the form is valid
    """
    data = {
        'title': 'test event',
        'description': 'test event description',
        'date': '2024-12-12 10:00'
    }
    form = CreateEventForm(data=data)
    assert form.validate(), "Form should be valid"

# TODO: Finish this test
def test_create_event_form_invalid_data(test_client, init_database):
    """
    GIVEN a Flask application instance
    WHEN the create event form input is invalid
    THEN check if the form is invalid
    """
    data = {
        'title': 'test event',
        'description': 'test event description',
        'date': '' # using 2024/12/12 passes along with other invalid options, although in the app it won't accept it
    }
    form = CreateEventForm(data=data)
    assert not form.validate(), "Form should be invalid with invalid date"

    # missing data
    data = {}
    form = CreateEventForm(data=data)
    assert not form.validate(), "Form should be invalid with invalid title and description"
    assert 'This field is required.' in form.title.errors
    assert 'This field is required.' in form.description.errors
    assert 'This field is required.' in form.date.errors

def test_add_member_form_valid_data(test_client, init_database):
    """
    GIVEN a Flask application instance
    WHEN the add member form input is valid
    THEN check if the form is valid
    """
    data = {
        'email': 'test@example.com'
    }
    form = AddMemberForm(data=data)
    assert form.validate(), "Form should be valid"

def test_add_member_form_invalid_data(test_client, init_database):
    """
    GIVEN a Flask application instance
    WHEN the add member form input is invalid
    THEN check if the form is invalid
    """
    data = {
        'email': 'testexample.com'
    }
    form = AddMemberForm(data=data)
    assert not form.validate(), "Form should be invalid with invalid email"

    # missing data
    data = {}
    form = AddMemberForm(data=data)
    assert not form.validate(), "Form should be invalid with invalid email"
    assert 'This field is required.' in form.email.errors