import pytest
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from api.models.blogmodels import db, BlogPost, User
from api.routes.blogroutes import blog_bp

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/testdb'
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.register_blueprint(blog_bp)
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_blog_post(client):
    user = User(username='testuser', email='test@example.com', password='password', firstname='First', lastname='Last')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()

    response = client.post('/api/v1/blog_posts', json={
        'title': 'Test Post',
        'content': 'This is a test post.',
        'author_id': str(user.id)
    })

    assert response.status_code == 201
    assert b'Test Post' in response.data


def test_get_blog_post(client):
    user = User(username='testuser', email='test@example.com', password='password', firstname='First', lastname='Last')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()

    post = BlogPost(title='Test Post', content='This is a test post.', author_id=user.id)
    db.session.add(post)
    db.session.commit()

    response = client.get(f'/api/v1/blog_posts/{post.id}')

    assert response.status_code == 200
    assert b'Test Post' in response.data


def test_update_blog_post(client):
    user = User(username='testuser', email='test@example.com', password='password', firstname='First', lastname='Last')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()

    post = BlogPost(title='Test Post', content='This is a test post.', author_id=user.id)
    db.session.add(post)
    db.session.commit()

    response = client.put(f'/api/v1/blog_posts/{post.id}', json={
        'title': 'Updated Post',
        'content': 'This is an updated test post.'
    })

    assert response.status_code == 200
    assert b'Updated Post' in response.data
