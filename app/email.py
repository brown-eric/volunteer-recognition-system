# app/email.py
from flask_mail import Message
from app.extensions import mail


def send_volunteer_registration_email(user_email, user_name):
    """Function to send a registration email to a new volunteer."""
    msg = Message("Welcome to VolunteerConnect!",
                  sender="VolunteerConnect2024@gmail.com",
                  recipients=[user_email])
    msg.body = f"Hi {user_name},it looks like you are ready to Volunteer!\n\nThank you for registering for VolunteerConnect!"

    try:
        mail.send(msg)
        print(f"Registration email sent to {user_email}.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def send_org_admin_registration_email(user_email, user_name, user_password):
    msg = Message("ACTION REQUESTED: Finish account setup",
                  sender="VolunteerConnect2024@gmail.com",
                  recipients=[user_email])
    msg.body = f"Hi {user_name},\n\nYour VolunteerConnect account has been created. Your temporary password is {user_password}.\n\nAfter logging in, please change your password."

    try:
        mail.send(msg)
        print(f"Registration email sent to {user_email}.")
    except Exception as e:
        print(f"Failed to send email: {e}")