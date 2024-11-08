import pytest_flask
import pytest
from app import create_app
from app.models import db

@pytest.fixture
def app():
    app = create_app('testing')
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
    with app.app_context():
        db.create_all()
        yield app

        # Close the database session and drop all tables after the session
        db.session.remove()
        db.drop_all()
    return app
#
# # from https://pytest-with-eric.com/api-testing/pytest-flask-postgresql-testing/#Use-an-in-memory-database-SQLite
# def pytest_addoption(parser):
#     parser.addoption(
#         "--dburl",  # For Postgres use "postgresql://user:password@localhost/dbname"
#         action="store",
#         default="sqlite:///:memory:",  # Default uses SQLite in-memory database
#         help="Database URL to use for tests.",
#     )
#
#
# @pytest.fixture(scope="session")
# def db_url(request):
#     """Fixture to retrieve the database URL."""
#     return request.config.getoption("--dburl")
#
#
# @pytest.hookimpl(tryfirst=True)
# def pytest_sessionstart(session):
#     db_url = session.config.getoption("--dburl")
#     try:
#         # Attempt to create an engine and connect to the database.
#         engine = create_engine(
#             db_url,
#             poolclass=StaticPool,
#         )
#         connection = engine.connect()
#         connection.close()  # Close the connection right after a successful connect.
#         print("Using Database URL:", db_url)
#         print("Database connection successful.....")
#     except SQLAlchemyOperationalError as e:
#         print(f"Failed to connect to the database at {db_url}: {e}")
#         pytest.exit(
#             "Stopping tests because database connection could not be established."
#         )
# @pytest.fixture(scope="session")
# def app():
#     """Session-wide test 'app' fixture."""
#     test_config = {
#         "SQLALCHEMY_DATABASE_URI": "sqlite:///database.db",
#         "SQLALCHEMY_TRACK_MODIFICATIONS": False,
#         "WTF_CSRF_ENABLED": False
#     }
#     app = create_app(test_config)
#     # app.config['WTF_CSRF_ENABLED'] = False  # for testing, we disable CSRF
#
#     with app.app_context():
#         db.create_all()
#         yield app
#
#         # Close the database session and drop all tables after the session
#         db.session.remove()
#         db.drop_all()
#     return app
#
# # from https://flask.palletsprojects.com/en/3.0.x/testing/
# @pytest.fixture
# def client(app):
#     """Test client for the app."""
#     return app.test_client()
#
# @pytest.fixture()
# def runner(app):
#     return app.test_cli_runner()
#
# @pytest.fixture
# def user_payload():
#     suffix = random.randint(1, 100)
#     return {
#         "name": f"JohnDoe",
#         "email": f"john_{suffix}@doe.com",
#         "password": f"password{suffix}",
#         "confirm_password": f"password{suffix}",
#         "role": f"volunteer"
#     }
