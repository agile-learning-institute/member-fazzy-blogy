import pytest
from api.app import app
from api.models.blogmodels import db, User
from api.config import TestConfig
from flask_jwt_extended import create_access_token


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


@pytest.fixture
def auth_headers(client):
    user = User(username='testuser', email='test@example.com', firstname='Test', lastname='User')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()
    token = create_access_token(identity=user.id)
    return {'Authorization': f'Bearer {token}'}


def test_create_blog_post(client, auth_headers):
    # Successful creation
    response = client.post('/api/v1/blog_posts', json={
        'title': 'New Post',
        'content': 'This is a new blog post',
        'author_id': 'valid-uuid'
    }, headers=auth_headers)
    assert response.status_code == 201
    assert response.json['message'] == 'Blog post created successfully'

    # Missing fields
    response = client.post('/api/v1/blog_posts', json={}, headers=auth_headers)
    assert response.status_code == 400
    assert response.json['error'] == 'Missing required fields'


def test_get_blog_posts(client, auth_headers):
    response = client.get('/api/v1/blog_posts?page=1&per_page=10', headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json['posts'], list)

    # Test invalid pagination parameters
    response = client.get('/api/v1/blog_posts?page=0&per_page=10', headers=auth_headers)
    assert response.status_code == 400
    assert response.json['error'] == 'Invalid pagination parameters'

def test_get_blog_post(client, auth_headers):
    response = client.get('/api/v1/blog_posts/valid-post-id', headers=auth_headers)
    assert response.status_code == 200
    assert 'title' in response.json

    # Non-existent post
    response = client.get('/api/v1/blog_posts/invalid-id', headers=auth_headers)
    assert response.status_code == 404

def test_update_blog_post(client, auth_headers):
    response = client.put('/api/v1/blog_posts/valid-post-id', json={
        'title': 'Updated Title'
    }, headers=auth_headers)
    assert response.status_code == 200
    assert response.json['post']['title'] == 'Updated Title'

    # No fields to update
    response = client.put('/api/v1/blog_posts/valid-post-id', json={}, headers=auth_headers)
    assert response.status_code == 400
    assert response.json['error'] == 'Missing fields to update'

def test_delete_blog_post(client, auth_headers):
    response = client.delete('/api/v1/blog_posts/valid-post-id', headers=auth_headers)
    assert response.status_code == 200
    assert response.json['message'] == 'Blog post deleted successfully'

    # Non-existent post
    response = client.delete('/api/v1/blog_posts/invalid-id', headers=auth_headers)
    assert response.status_code == 404
