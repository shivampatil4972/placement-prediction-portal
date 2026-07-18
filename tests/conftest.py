import pytest
import sys
import os

# Add the parent directory to sys.path to allow imports from the main app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from models.database import init_db

@pytest.fixture
def client():
    """A test client for the app."""
    app.config['TESTING'] = True
    # Use in-memory SQLite for testing to avoid touching real DB
    app.config['DATABASE'] = ':memory:'
    
    with app.test_client() as client:
        with app.app_context():
            # Init dummy DB for tests
            pass
        yield client
