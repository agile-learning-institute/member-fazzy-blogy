import json
from api.models.blogmodels import User

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
