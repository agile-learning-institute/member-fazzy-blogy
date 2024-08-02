import pytest
from api.app import app, db

@pytest.fixture(scope='module')
def test_client():
    app.config.from_object('config.TestConfig')
    testing_client = app.test_client()

    with app.app_context():
        db.create_all()

        yield testing_client

        db.drop_all()
