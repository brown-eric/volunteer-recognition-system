from venv import create
import pytest_flask

import pytest
from app import create_app

@pytest.fixture
def app():
    app = create_app('testing')
    create_app()