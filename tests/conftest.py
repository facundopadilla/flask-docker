import pytest
from flask_app.ext.application import create_app

@pytest.fixture(scope="function")
def fixture_create_app():
    """Instance of main flask app"""
    return create_app()
