# conftest.py
import pytest
from api.app import app
from api.models.blogmodels import db, User
from api.config import TestConfig
from flask_jwt_extended import create_access_token
from api.models.blogmodels import db, User, BlogPost, Comment


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

def test_create_comment(test_client, auth_header, new_blog_post):
    response = test_client.post(
        '/api/v1/comments',
        json={
            'blog_post_id': str(new_blog_post.id),
            'user_id': str(new_blog_post.author_id),
            'comment': 'This is a test comment'
        },
        headers=auth_header
    )
    assert response.status_code == 201
    assert response.json['message'] == 'Comment added successfully'
    assert response.json['comment']['comment'] == 'This is a test comment'


def test_get_comments_for_blog_post(test_client, auth_header, new_blog_post):
    response = test_client.get(
        f'/api/v1/blog_posts/{new_blog_post.id}/comments',
        headers=auth_header
    )
    assert response.status_code == 200
    assert 'comments' in response.json


def test_get_comment(test_client, auth_header, new_blog_post):
    # Create a comment first
    comment_response = test_client.post(
        '/api/v1/comments',
        json={
            'blog_post_id': str(new_blog_post.id),
            'user_id': str(new_blog_post.author_id),
            'comment': 'Another test comment'
        },
        headers=auth_header
    )
    comment_id = comment_response.json['comment']['id']

    # Fetch the comment
    response = test_client.get(f'/api/v1/comments/{comment_id}', headers=auth_header)
    assert response.status_code == 200
    assert response.json['comment'] == 'Another test comment'


def test_update_comment(test_client, auth_header, new_blog_post):
    # Create a comment first
    comment_response = test_client.post(
        '/api/v1/comments',
        json={
            'blog_post_id': str(new_blog_post.id),
            'user_id': str(new_blog_post.author_id),
            'comment': 'Comment to update'
        },
        headers=auth_header
    )
    comment_id = comment_response.json['comment']['id']

    # Update the comment
    update_response = test_client.put(
        f'/api/v1/comments/{comment_id}',
        json={'comment': 'Updated comment'},
        headers=auth_header
    )
    assert update_response.status_code == 200
    assert update_response.json['message'] == 'Comment updated successfully'
    assert update_response.json['comment']['comment'] == 'Updated comment'


def test_delete_comment(test_client, auth_header, new_blog_post):
    # Create a comment first
    comment_response = test_client.post(
        '/api/v1/comments',
        json={
            'blog_post_id': str(new_blog_post.id),
            'user_id': str(new_blog_post.author_id),
            'comment': 'Comment to delete'
        },
        headers=auth_header
    )
    comment_id = comment_response.json['comment']['id']

    # Delete the comment
    delete_response = test_client.delete(f'/api/v1/comments/{comment_id}', headers=auth_header)
    assert delete_response.status_code == 200
    assert delete_response.json['message'] == 'Comment deleted successfully'
