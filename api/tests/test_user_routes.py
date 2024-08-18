# test_user_routes.py
import json
import pytest
from uuid import uuid4
from sqlalchemy.exc import SQLAlchemyError
from api.models.blogmodels import User, db
from flask_jwt_extended import create_access_token

@pytest.fixture
def auth_header(client):
    access_token = create_access_token(identity='testuser')
    return {'Authorization': f'Bearer {access_token}'}

# User creation tests
def test_create_user_success(client):
    user_data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password123',
        'firstname': 'Test',
        'lastname': 'User',
        'role': 'user'
    }
    response = client.post('/api/v1/users', data=json.dumps(user_data), content_type='application/json')
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'User created successfully'
    assert data['username'] == 'testuser'
    assert data['email'] == 'testuser@example.com'
    assert data['firstname'] == 'Test'
    assert data['lastname'] == 'User'
    assert data['role'] == 'user'

def test_create_user_missing_fields(client):
    user_data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password123'
    }
    response = client.post('/api/v1/users', data=json.dumps(user_data), content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Missing required fields'

def test_create_user_invalid_email(client):
    user_data = {
        'username': 'testuser',
        'email': 'invalid-email',
        'password': 'password123',
        'firstname': 'Test',
        'lastname': 'User',
        'role': 'user'
    }
    response = client.post('/api/v1/users', data=json.dumps(user_data), content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'Invalid email address'

def test_create_user_duplicate_user(client):
    user_data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password123',
        'firstname': 'Test',
        'lastname': 'User',
        'role': 'user'
    }
    # Create the first user
    response = client.post('/api/v1/users', data=json.dumps(user_data), content_type='application/json')
    assert response.status_code == 201

    # Attempt to create the same user again
    response = client.post('/api/v1/users', data=json.dumps(user_data), content_type='application/json')
    assert response.status_code == 409
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'User with that username or email already exists'

# Get users route tests
def test_get_users_success(client, setup_database, auth_header):
    response = client.get('/api/v1/users', headers=auth_header, query_string={'page': 1, 'per_page': 10})
    assert response.status_code == 200
    data = response.get_json()
    assert 'users' in data
    assert 'total' in data
    assert 'pages' in data
    assert 'current_page' in data
    assert 'next_page' in data
    assert 'prev_page' in data
    assert len(data['users']) == 10, f"Expected 10 users, got {len(data['users'])}"

# def test_get_users_invalid_page(client, setup_database, auth_header):
#     response = client.get('/api/v1/users', headers=auth_header, query_string={'page': 'invalid', 'per_page': 10})
#     assert response.status_code == 400

def test_get_users_unauthorized(client):
    response = client.get('/api/v1/users')
    assert response.status_code == 401
    data = response.get_json()
    assert 'msg' in data
    assert data['msg'] == 'Missing Authorization Header'

# def test_get_users_pagination(client, setup_database, auth_header):
#     response = client.get('/api/v1/users', headers=auth_header, query_string={'page': 2, 'per_page': 10})
#     assert response.status_code == 200
#     data = response.get_json()
#     assert 'users' in data
#     assert len(data['users']) == 10, f"Expected 10 users, got {len(data['users'])}"


def test_get_users_large_page_number(client, setup_database, auth_header):
    response = client.get('/api/v1/users', headers=auth_header, query_string={'page': 999, 'per_page': 10})
    assert response.status_code == 200
    data = response.get_json()
    assert 'users' in data
    assert len(data['users']) == 0, f"Expected 0 users, got {len(data['users'])}"

# test longin routes
def test_login_success(test_client):
    response = test_client.post('/api/v1/login', json={
        'identifier': 'john_doe',
        'password': 'securepassword123'
    })

    data = response.get_json()
    assert response.status_code == 200
    assert 'access_token' in data
    assert data['message'] == 'Login successful'

def test_login_failure(test_client):
    response = test_client.post('/api/v1/login', json={
        'identifier': 'john_doe',
        'password': 'wrongpassword'
    })

    data = response.get_json()
    assert response.status_code == 401
    assert data['message'] == 'Invalid username or password'

def test_login_missing_fields(test_client):
    response = test_client.post('/api/v1/login', json={})

    data = response.get_json()
    assert response.status_code == 400
    assert data['message'] == 'Missing required fields'

def get_access_token(client, username, password):
    response = client.post('/api/v1/login', json={
        'username': username,
        'password': password
    })
    return response.get_json()['access_token']


# Test Update user
def test_update_user(client, token):
    user_id = str(uuid4())

    user = User(
        id=user_id,
        username="testuser",
        email="testuser@example.com",
        firstname="Test",
        lastname="User",
        role="user",
        is_active=True
    )
    user.set_password("password")
    db.session.add(user)
    db.session.commit()

    # Update the user
    response = client.put(
        f'/api/v1/update/{user_id}',
        headers={"Authorization": f"Bearer {token}"},
        data=json.dumps({
            "username": "updateduser",
            "email": "updateduser@example.com",
            "is_active": False,
            "role": "user"
        }),
        content_type='application/json'
    )
    assert response.status_code == 200
    response_json = response.get_json()
    assert response_json['username'] == "updateduser"
    assert response_json['email'] == "updateduser@example.com"
    assert response_json['is_active'] is False
    assert response_json['role'] == "user"


def test_get_user(test_client, init_database):
    """Test fetching a user by user_id."""
    response = test_client.get('/users/44040d26-2fc9-4e5f-b577-97ba9e771392')
    assert response.status_code == 200

    user_data = response.get_json()
    assert user_data['id'] == "44040d26-2fc9-4e5f-b577-97ba9e771392"
    assert user_data['username'] == "testuser"
    assert user_data['email'] == "testuser@example.com"
    assert user_data['firstname'] == "Test"
    assert user_data['lastname'] == "User"
    assert user_data['role'] == "admin"
    assert user_data['created_at'] is not None


def test_get_user_not_found(test_client, init_database):
    """Test fetching a non-existent user."""
    response = test_client.get('/users/invalid-user-id')
    assert response.status_code == 404


def test_database_error(test_client, init_database, mocker):
    """Test handling a database error."""
    mocker.patch('app.models.User.query.get_or_404', side_effect=SQLAlchemyError())

    response = test_client.get('/users/44040d26-2fc9-4e5f-b577-97ba9e771392')
    assert response.status_code == 500
    error_data = response.get_json()
    assert 'error' in error_data
    assert error_data['error'] == 'Database error occurred'