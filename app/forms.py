
# Flask modules
from flask_wtf import FlaskForm
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Regexp, NumberRange
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, TextAreaField, DateTimeField

# Local modules
from app.models import User, HoursLog, Event

# TODO: Whitelist or blacklist or escape sanitize field inputs, find a function for this
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=64)], render_kw={'placeholder': 'example@email.com'})
    password = PasswordField('Password', validators=[DataRequired(), Length(max=64)], render_kw={'placeholder': '********'})
    remember_me = BooleanField('Remember me', default=False)
    submit = SubmitField('Log In')

# testing
def validate_email(form, email):
    existing_user = User.query.filter_by(email=email.data).one_or_none()
    if existing_user:
        raise ValidationError('Email address already registered.')

# testing
# TODO: Add a password dictionary check
def validate_password(self, password):
    if not any(c.isalpha() for c in password.data) or not any(c.isdigit() for c in password.data):
        raise ValidationError('Password must contain at least one letter and one digit.')

class RegistrationForm(FlaskForm):
    name = StringField('Username', validators=[
        DataRequired(),
        Length(min=2, max=80),
        Regexp(r'^[a-zA-Z0-9_]+$', message='Username must contain only letters, numbers, and underscores.')],
                       render_kw={'placeholder': 'Display name'})
    email = StringField('Email', validators=[
        DataRequired(), Length(max=64),
        Email(), validate_email # testing validate_email
    ], render_kw={'placeholder': 'example@email.com'})
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, max=64), validate_password # testing validate_password
    ], render_kw={'placeholder': 'Enter your password'})
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), Length(max=64),
        EqualTo('password', message='Passwords must match')
        ],
                                     render_kw={'placeholder': 'Confirm your password'})
    role = SelectField('Are you a', choices=[('volunteer', 'Volunteer'), ('volunteering organization', 'Volunteering Organization'),
                                             ('admin', 'Admin')], validators=[DataRequired()])
    submit = SubmitField('Register')

class EditProfileForm(FlaskForm):
    name = StringField('Username', validators=[
        DataRequired(),
        Length(min=2, max=80),
        Regexp(r'^[a-zA-Z0-9_]+$', message='Username must contain only letters, numbers, and underscores.')],
                       render_kw={'placeholder': 'Display name'})
    email = StringField('Email', validators=[
        DataRequired(),
        Email(), Length(max=64)
    ], render_kw={'placeholder': 'example@email.com'})
    submit = SubmitField('Save Changes')


class AddHoursForm(FlaskForm):
    email = StringField('User Email', validators=[DataRequired(), Email(), Length(max=64)])
    # we don't have to implement this, but an important thing to keep in mind is that only whole hours will be accepted, not increments.
    # set an input range so there is no undefined behavior. IntegerField is prone to error without setting number range restrictions
    hours = IntegerField('Hours to Add', validators=[DataRequired(), NumberRange(min=1, max=10000, message="Hours must be greater than 0")])
    submit = SubmitField('Add Hours')

class AddUserForm(FlaskForm):
    name = StringField('Username', validators=[
        DataRequired(),
        Length(min=2, max=80),
        Regexp(r'^[a-zA-Z0-9_]+$', message='Username must contain only letters, numbers, and underscores.')],
                       render_kw={'placeholder': 'Display name'})
    email = StringField('Email', validators=[
        DataRequired(), Length(max=64),
        Email(), validate_email  # testing validate_email
    ], render_kw={'placeholder': 'example@email.com'})
    role = SelectField('Role',
                       choices=[('volunteering organization', 'Volunteering Organization'),
                                ('admin', 'Admin')], validators=[DataRequired()])
    submit = SubmitField('Register')

class RemoveUserForm(FlaskForm):
    email = StringField('User Email', validators=[DataRequired(), Email(), Length(max=64)])
    submit = SubmitField('Remove User')

class CreateEventForm(FlaskForm):
    title = StringField('Event Title', validators=[DataRequired(), Length(max=80)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=300)])
    date = DateTimeField('Event Date (YYYY-MM-DD HH:MM)', format='%Y-%m-%d %H:%M', validators=[DataRequired()], description="Input date and time in proper format: YYYY-MM-DD HH:MM")
    submit = SubmitField('Create Event')

class AddMemberForm(FlaskForm):
    email = StringField('User Email', validators=[DataRequired(), Email(), Length(max=64)])
    submit = SubmitField('Add Volunteer To Your Organization')
