
# Flask modules
from flask_wtf import FlaskForm
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Regexp, NumberRange
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField

# Local modules
from app.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'placeholder': 'example@email.com'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder': '********'})
    remember_me = BooleanField('Remember me', default=False)
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(),
        Length(min=2, max=80),
        Regexp(r'^[a-zA-Z0-9_]+$', message='Name must contain only letters, numbers, and underscores.')],
                       render_kw={'placeholder': 'Display name'})
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ], render_kw={'placeholder': 'example@email.com'})
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8),
    ], render_kw={'placeholder': 'Enter your password'})
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ],
                                     render_kw={'placeholder': 'Confirm your password'})
    # VULN: No controls to prevent any user from registering as an org or admin
    role = SelectField('Are you a', choices=[('volunteer', 'Volunteer'), ('volunteering organization', 'Volunteering Organization'),
                                             ('admin', 'Admin')], validators=[DataRequired()])
    submit = SubmitField('Register')

    # CHECK: Are these functions being called?
    def validate_email(self, email):
        existing_user = User.query.filter_by(email=email.data).one_or_none()
        if existing_user:
            raise ValidationError('Email address already registered.')

    def validate_password(self, password):
        if not any(c.isalpha() for c in password.data) or not any(c.isdigit() for c in password.data):
            raise ValidationError('Password must contain at least one letter and one digit.')

class EditProfileForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(),
        Length(min=2, max=80),
        Regexp(r'^[a-zA-Z0-9_]+$', message='Name must contain only letters, numbers, and underscores.')],
                       render_kw={'placeholder': 'Display name'})
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ], render_kw={'placeholder': 'example@email.com'})
    submit = SubmitField('Save Changes')


class AddHoursForm(FlaskForm):
    email = StringField('User Email', validators=[DataRequired(), Email()])
    hours = IntegerField('Hours to Add', validators=[DataRequired(), NumberRange(min=1, message="Hours must be greater than 0")])
    submit = SubmitField('Add Hours')

class RemoveUserForm(FlaskForm):
    email = StringField('User Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Remove User')
