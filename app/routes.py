# Flask modules
from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import login_user, logout_user, current_user, login_required

# Local modules
from app.models import User
from app.extensions import db, bcrypt, login_manager
from app.forms import *

routes_bp = Blueprint('routes', __name__, url_prefix="/")


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).one_or_none()


@routes_bp.route("/")
@login_required
def home():
    return render_template('index.html')

@routes_bp.route("/information")
def info():
    return render_template('home.html')


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

    return render_template('edit_profile.html', form=form)



@routes_bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("routes.home"))

    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember_me = form.remember_me.data

        user = User.query.filter_by(email=email).one_or_none()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=remember_me)
            flash(f"Logged in successfully as {user.name}", 'success')
            return redirect(url_for("routes.home"))
        else:
            flash("Invalid email or password", 'danger')

    return render_template('auth/login.html', form=form)


@routes_bp.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("routes.home"))

    form = RegistrationForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        role = form.role.data

        hashed_password = bcrypt.generate_password_hash(password)

        # Add user to database
        new_user = User(name=name, email=email, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()

        #email confirmatino
        send_registration_email(email, name)

        # Login user
        login_user(new_user)

        flash(f'Account created successfully! You are now logged in as {new_user.name}.', 'success')
        return redirect(url_for("routes.home"))

    return render_template('auth/register.html', form=form)

@routes_bp.route("/user/<name>")
@login_required
def user_profile(name):
    user = User.query.filter_by(name=name).one_or_none()
    hours_logs = HoursLog.query.filter_by(added_to=user.email).all()
    return render_template('user.html', user=user, hours_logs=hours_logs)

@routes_bp.route("/rewards")
@login_required
def rewards():
    user = current_user
    rewards = [
        {'name': 'Bronze Badge', 'description': 'Awarded for 10 volunteer hours'},
        {'name': 'Silver Badge', 'description': 'Awarded for 20 volunteer hours'},
        {'name': 'Gold Badge', 'description': 'Awarded for 30 volunteer hours'},
        {'name': 'Platinum Badge', 'description': 'Awarded for 50 volunteer hours'},
    ]
    user_rewards = []
    if user.hours_volunteered >= 50:
        user_rewards.append(rewards[3])  # Platinum Badge
    if user.hours_volunteered >= 30:
        user_rewards.append(rewards[2])  # Gold Badge
    if user.hours_volunteered >= 20:
        user_rewards.append(rewards[1])  # Silver Badge
    if user.hours_volunteered >= 10:
        user_rewards.append(rewards[0])  # Bronze Badge

    return render_template('rewards.html', rewards=user_rewards)


@routes_bp.route("/add_hours", methods=['GET', 'POST'])
@login_required
def add_hours():
    if current_user.role == 'volunteer':
        flash('You do not have permission to add hours.', 'danger')
        return redirect(url_for('routes.home'))

    form = AddHoursForm()
    email_invalid = False  # Flag for invalid email

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
                                     added_by=current_user.email,
                                     added_to=user.email)
                db.session.add(log_entry)
                db.session.commit()

                flash(f'Successfully added {form.hours.data} hours to {user.name}.', 'success')
        else:
            # Flash message and set flag for invalid email
            flash('No user found with that email address. Please try again.', 'danger')
            email_invalid = True

        return redirect(url_for('routes.add_hours'))

    return render_template('add_hours.html', form=form, email_invalid=email_invalid)


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

    return render_template('remove_user.html', form=form)

@routes_bp.route("/view_database", methods=['GET', 'POST'])
@login_required
def view_database():
    if current_user.role != 'admin':
        flash('You do not have permission to view the database.', 'danger')
        return redirect(url_for('routes.home'))

    # Fetch all users or filter by email if a search is submitted
    if request.method == 'POST':
        search_email = request.form.get('search_email')
        users = User.query.filter(User.email.contains(search_email)).all()
    else:
        users = User.query.all()

    return render_template('view_database.html', users=users)





@routes_bp.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for("routes.login"))