import pytest_flask
import pytest
from app import create_app
from app.models import db, User
from app.extensions import bcrypt

@pytest.fixture(scope='module')
def app():
    app = create_app('testing')
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing

    # Bind Bcrypt and LoginManager to the app
    bcrypt.init_app(app)
    #login_manager.init_app(app)

    with app.app_context():
        db.create_all()
        yield app

        # Close the database session and drop all tables after the session
        db.session.remove()
        db.drop_all()
    return app

@pytest.fixture(scope='module')
def test_client(app):
    return app.test_client()

@pytest.fixture(scope='module')
def init_database():
    hashed_password = bcrypt.generate_password_hash('password123').decode('utf-8')
    user = User(name='testvolunteer', email='testvolunteer@example.com', password=hashed_password, role='volunteer')
    db.session.add(user)
    db.session.commit()