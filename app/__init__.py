# Flask modules
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


def create_app(debug: bool = False) -> Flask:
    # Initialize app
    app = Flask(__name__, template_folder='../templates', static_folder='../static', static_url_path='/')

    # Setup app configs
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = "YOUR-SECRET-KEY-HERE"
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Replace with your SMTP server
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = 'VolunteerConnect2024@gmail.com'  # Replace with your email
    app.config['MAIL_PASSWORD'] = 'exhqpnxdzddeqswh'  # Replace with your email password
    app.config['MAIL_DEFAULT_SENDER'] = 'VolunteerConnect2024@gmail.com'

    # Initialize extensions
    from app.extensions import db, bcrypt, csrf, login_manager
    with app.app_context():
        db.init_app(app)
    csrf.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate = Migrate(app, db)

    # Create database tables
    from app import models
    with app.app_context():
        db.create_all()

    # Register blueprints
    from app.routes import routes_bp
    # Limiter https://flask-limiter.readthedocs.io/en/stable/recipes.html
    limiter = Limiter(get_remote_address, app=app, default_limits=["5/second"])
    limiter.limit("5/second")(routes_bp)
    app.register_blueprint(routes_bp)


    #email
    from app.extensions import mail
    mail.init_app(app)
    return app
