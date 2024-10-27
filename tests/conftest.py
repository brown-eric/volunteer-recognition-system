import pytest_flask

import pytest
from app import create_app
from app.models import db
from app.models import User

# from https://pytest-with-eric.com/api-testing/pytest-flask-postgresql-testing/#Use-an-in-memory-database-SQLite
@pytest.fixture(scope="session")
def app():
    """Session-wide test 'app' fixture."""
    test_config = {
        "SQLALCHEMY_DATABASE_URI": "sqlite:///database.db",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    }
    app = create_app(test_config)

    with app.app_context():
        db.create_all()
        yield app

        # Close the database session and drop all tables after the session
        db.session.remove()
        db.drop_all()

# from https://flask.palletsprojects.com/en/3.0.x/testing/
@pytest.fixture
def test_client(app):
    """Test client for the app."""
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
