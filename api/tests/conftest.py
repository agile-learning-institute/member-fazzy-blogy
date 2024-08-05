# conftest.py
import pytest
from api.app import app
from api.models.blogmodels import db, User
from api.config import TestConfig

@pytest.fixture
def client():
    app.config.from_object(TestConfig)
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

@pytest.fixture(scope='module')
def setup_database():
    with app.app_context():
        db.create_all()
        # Create test users
        users = [
            User(username=f'user{i}', email=f'user{i}@example.com', password='password', firstname=f'First{i}', lastname=f'Last{i}', role='user')
            for i in range(1, 26)
        ]
        db.session.bulk_save_objects(users)
        db.session.commit()
        yield
        db.session.remove()
        db.drop_all()
