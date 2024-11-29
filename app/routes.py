# Flask modules
#from crypt import methods
import string
import secrets
from markupsafe import escape
from flask import Blueprint, redirect, url_for, render_template, flash, request, make_response, jsonify
from flask_login import login_user, logout_user, current_user, login_required

from app.email import send_volunteer_registration_email, send_org_admin_registration_email

alphabet = string.ascii_letters + string.digits
# Local modules
from app.extensions import db, bcrypt, login_manager
from app.forms import *

routes_bp = Blueprint('routes', __name__, url_prefix="/")


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).one_or_none()

# https://flask-limiter.readthedocs.io/en/stable/recipes.html
@routes_bp.errorhandler(429)
def ratelimit_handler(e):
    return make_response(
            jsonify(error=f"ratelimit exceeded {e.description}")
            , 429
    )

@routes_bp.route("/")
@login_required
def home():
    return render_template('index.html', active_tab='home')

@routes_bp.route("/information")
def info():
    return render_template('home.html', active_tab='info')


@routes_bp.route("/edit_profile", methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()

    if form.validate_on_submit():
        # Do not change data if field is left empty. Need to test this
        if form.name.data: current_user.name = form.name.data
        if form.email.data: current_user.email = form.email.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('routes.user_profile', name=current_user.name))

    # Pre-populate the form with the current user's data
    form.name.data = current_user.name
    form.email.data = current_user.email

    return render_template('edit_profile.html', form=form, active_tab='profile')


@routes_bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("routes.home"))

    form = LoginForm()

    if form.validate_on_submit():
        """ https://flask.palletsprojects.com/en/stable/quickstart/ """
        email = escape(form.email.data)
        password = escape(form.password.data)
        remember_me = form.remember_me.data

        user = User.query.filter_by(email=email).one_or_none()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=remember_me)
            flash(f"Logged in successfully as {user.name}", 'success')
            return redirect(url_for("routes.home"))
        else:
            flash("Invalid email or password", 'danger')

    return render_template('auth/login.html', form=form, active_tab='login')


@routes_bp.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("routes.home"))

    form = RegistrationForm()

    if form.validate_on_submit():
        name = escape(form.name.data)
        email = escape(form.email.data)
        password = escape(form.password.data)
        role = form.role.data

        hashed_password = bcrypt.generate_password_hash(password)

        # Add user to database
        new_user = User(name=name, email=email, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()

        #email confirmation
        send_volunteer_registration_email(email, name)

        # Login user
        login_user(new_user)

        flash(f'Account created successfully! You are now logged in as {new_user.name}.', 'success')
        return redirect(url_for("routes.home"))

    return render_template('auth/register.html', form=form)

@routes_bp.route("/user/<name>")
@login_required
def user_profile(name):
    # Remediated IDOR vuln
    if current_user.name != name:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('routes.home'))
    user = User.query.filter_by(name=name).one_or_none()
    hours_logs = HoursLog.query.filter_by(added_to=user.email).all()
    return render_template('user.html', user=user, hours_logs=hours_logs, active_tab='profile')

@routes_bp.route("/leaderboard")
@login_required
def leaderboard():
    # Retrieve all volunteers ordered by hours in descending order
    volunteers = User.query.filter_by(role='volunteer').order_by(User.hours_volunteered.desc()).all()
    return render_template('leaderboard.html', volunteers=volunteers, active_tab='leaderboard')

@routes_bp.route("/rewards")
@login_required
def rewards():
    if current_user.role != 'volunteer':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('routes.home'))

    user = current_user
    total_hours = user.hours_volunteered
    rewards = [
        {'name': 'Bronze Badge', 'description': 'Awarded for 10 volunteer hours', 'threshold': 10},
        {'name': 'Silver Badge', 'description': 'Awarded for 20 volunteer hours', 'threshold': 20},
        {'name': 'Gold Badge', 'description': 'Awarded for 30 volunteer hours', 'threshold': 30},
        {'name': 'Platinum Badge', 'description': 'Awarded for 50 volunteer hours', 'threshold': 50},
    ]

    user_rewards = [reward for reward in rewards if total_hours >= reward['threshold']]
    next_reward = next((reward for reward in rewards if total_hours < reward['threshold']), None)

    progress = 0
    if next_reward:
        progress = (total_hours / next_reward['threshold']) * 100

    return render_template(
        'rewards.html',
        rewards=user_rewards,
        next_reward=next_reward,
        progress=progress,
        active_tab='rewards'
    )



@routes_bp.route("/add_hours", methods=['GET', 'POST'])
@login_required
def add_hours():
    """ Only volunteering organization accounts can add hours """
    if current_user.role != 'volunteering organization':
        flash('You do not have permission to add hours.', 'danger')
        return redirect(url_for('routes.home'))

    form = AddHoursForm()
    email_invalid = False  # Flag for invalid email

    volunteer_emails = User.query.with_entities(User.email).all()
    # Convert the query result to a list of strings
    email_list = [email.email for email in volunteer_emails]


    if form.validate_on_submit():
        # Find the user by email
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            # Check if the user is a volunteer
            if user.role != 'volunteer':
                flash(f'Cannot add hours. {user.name} is not a volunteer.', 'danger')
            else:
                # Add hours to the user's total
                user.hours_volunteered += form.hours.data
                db.session.commit()  # Commit the changes to the database

                # Log the addition of hours
                log_entry = HoursLog(hours_added=form.hours.data,
                                     added_by_email=current_user.email,
                                     added_by_username=current_user.name,
                                     added_to=user.email)
                db.session.add(log_entry)
                db.session.commit()

                flash(f'Successfully added {form.hours.data} hours to {user.name}.', 'success')
        else:
            # Flash message and set flag for invalid email
            flash('No user found with that email address. Please try again.', 'danger')
            email_invalid = True

        return redirect(url_for('routes.add_hours'))

    # volunteer_emails = User.query.with_entities(User.email).all()
    # email_list = [email.email for email in volunteer_emails if email.role == "volunteer"]
    email_list = [volunteer.email for volunteer in current_user.volunteers if volunteer.role == 'volunteer']
    return render_template('add_hours.html', form=form, email_invalid=email_invalid, active_tab='add-hours', email_data=email_list)


@routes_bp.route("/add_user", methods=['GET', 'POST'])
@login_required
def add_user():
    if current_user.role != 'admin':
        flash('You do not have permission to add users.', 'danger')
        return redirect(url_for('routes.home'))

    form = AddUserForm()

    if form.validate_on_submit():
        name = escape(form.name.data)
        email = escape(form.email.data)
        role = form.role.data

        """ https://docs.python.org/3/library/secrets.html """
        while True:
            password = ''.join(secrets.choice(alphabet) for i in range(10))
            if (any(c.islower() for c in password)
                    and any(c.isupper() for c in password)
                    and sum(c.isdigit() for c in password) >= 3):
                break

        hashed_password = bcrypt.generate_password_hash(password)

        # Add user to database
        new_user = User(name=name, email=email, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()

        send_org_admin_registration_email(email, name, password)

    return render_template('add_user.html', form=form)

@routes_bp.route("/remove_user", methods=['GET', 'POST'])
@login_required
def remove_user():
    if current_user.role != 'admin':
        flash('You do not have permission to remove users.', 'danger')
        return redirect(url_for('routes.home'))

    form = RemoveUserForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).one_or_none()

        if user:
            db.session.delete(user)
            db.session.commit()
            flash(f'User {user.name} has been removed from the system.', 'success')
        else:
            flash('User not found.', 'danger')

        return redirect(url_for('routes.remove_user'))

    return render_template('remove_user.html', form=form, active_tab='remove-user')

@routes_bp.route("/view_database", methods=['GET', 'POST'])
@login_required
def view_database():
    if current_user.role != 'admin':
        flash('You do not have permission to view the database.', 'danger')
        return redirect(url_for('routes.home'))

    # get all users or filter by email if a search is submitted
    if request.method == 'POST':
        search_email = request.form.get('search_email')
        users = User.query.filter(User.email.contains(search_email)).all()
    else:
        users = User.query.all()

    return render_template('view_database.html', users=users, active_tab='database')

@routes_bp.route("/create_event", methods=['GET', 'POST'])
@login_required
def create_event():
    if current_user.role != 'volunteering organization':
        flash('You do not have permission to create events.', 'danger')
        return redirect(url_for('routes.home'))

    form = CreateEventForm()

    if form.validate_on_submit():
        new_event = Event(
            title=form.title.data,
            description=form.description.data,
            date=form.date.data,
            created_by=current_user.name  # do i want email or name?
        )
        db.session.add(new_event)
        db.session.commit()
        flash('Event created successfully!', 'success')
        return redirect(url_for('routes.create_event'))

    return render_template('create_event.html', form=form, active_tab='create-event')

@routes_bp.route("/events")
@login_required
def events():
    # Fetch all events from the database
    events = Event.query.order_by(Event.date).all()
    return render_template('events.html', events=events, active_tab='events')

@routes_bp.route("/signup_event/<int:event_id>")
@login_required
def signup_event(event_id):
    event = Event.query.get(event_id)

    if current_user.role != 'volunteer':
        flash('Only volunteers can sign up for events.', 'danger')
        return redirect(url_for('routes.events'))

    if event:
        event.attendees.append(current_user)
        db.session.commit()
        flash('Successfully signed up for the event!', 'success')
    else:
        flash('Event not found.', 'danger')

    return redirect(url_for('routes.events'))

@routes_bp.route("/add_member", methods=['GET', 'POST'])
@login_required
def add_member():

    form = AddMemberForm()
    email_invalid = False  # Flag for invalid email

    if form.validate_on_submit():
        # Find the user by email
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            # Check if the user is a volunteer
            if user.role != 'volunteer':
                flash(f'Cannot add member. {user.name} is not a volunteer.', 'danger')
            else:
                # Add the member
                current_user.volunteers.append(user)
                db.session.commit()  # Commit the changes to the database

                # Log the addition of hours

                flash(f'Successfully added {user.name}.', 'success')
        else:
            # Flash message and set flag for invalid email
            flash('No user found with that email address. Please try again.', 'danger')
            email_invalid = True

        return redirect(url_for('routes.add_member'))

    return render_template('manage_memberships.html', form=form, email_invalid=email_invalid, active_tab='manage-memberships')

@routes_bp.route("/remove_member/<int:volunteer_id>", methods=['GET', 'POST'])
@login_required
def remove_member(volunteer_id):
    if current_user.role != 'volunteering organization':
        flash('You do not have permission to remove a member.', 'danger')
        return redirect(url_for('routes.home'))
    volunteer = User.query.filter_by(id=volunteer_id, role='volunteer').first()
    if volunteer.role != 'volunteer':
        flash('This user is not a volunteer.', 'danger')
        return redirect(url_for('routes.remove_member'))

    form=AddMemberForm()
    email_invalid = False

    if volunteer in current_user.volunteers:
        # Remove the given volunteer
        current_user.volunteers.remove(volunteer)
        db.session.commit()

        flash(f'Successfully removed {volunteer.name}.', 'success')
    else:
        # Flash message and set flag for invalid email
        flash('This user is not a member of your organization', 'danger')
        return redirect(url_for('routes.remove_member'))
    return render_template('manage_memberships.html', form=form, active_tab='manage-memberships')

@routes_bp.route("/remove_org/<int:org_id>", methods=['GET', 'POST'])
@login_required
def remove_org(org_id):
    if current_user.role != 'volunteer':
        flash('You are not a volunteer.', 'danger')
        return redirect(url_for('routes.home'))
    org = User.query.filter_by(id=org_id, role='volunteering organization').first()
    if org.role != 'volunteering organization':
        flash('This user is not an organization.', 'danger')
        return redirect(url_for('routes.remove_org'))

    form=AddMemberForm()
    email_invalid = False

    if org in current_user.organizations:
        # Remove the given volunteer
        current_user.organizations.remove(org)
        db.session.commit()

        flash(f'Successfully removed {org.name}.', 'success')
    else:
        # Flash message and set flag for invalid email
        flash('You are not a member of this organization', 'danger')
        return redirect(url_for('routes.remove_org'))
    return render_template('manage_memberships.html', form=form, active_tab='manage-memberships')

@routes_bp.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for("routes.login"))