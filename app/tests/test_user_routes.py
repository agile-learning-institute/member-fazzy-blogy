import json
import pytest
from ..app import db
from app.models import User

@pytest.fixture
def access_token(test_client):
    # Create a user
    test_client.post('/users', data=json.dumps({
        'username': 'testuser',
        'email': 'test@example.com',
        'password_hash': 'hashedpassword'
    }), content_type='application/json')

    # Log in to get the access token
    response = test_client.post('/login', data=json.dumps({
        'username': 'testuser',
        'password': 'hashedpassword'
    }), content_type='application/json')

    data = json.loads(response.data)
    return data['access_token']

# Create a user with authentication
def test_create_user(test_client, access_token):
    response = test_client.post('/users', data=json.dumps({
        'username': 'newuser',
        'email': 'new@example.com',
        'password_hash': 'newhashedpassword'
    }), headers={'Authorization': f'Bearer {access_token}'}, content_type='application/json')

    assert response.status_code == 201
    assert b'User created successfully' in response.data

    # Verify the user was created
    user = User.query.filter_by(username='newuser').first()
    assert user is not None
    assert user.email == 'new@example.com'
    assert user.password_hash == 'newhashedpassword'

# Create a user without authentication
def test_create_user_unauthorized(test_client):
    response = test_client.post('/users', data=json.dumps({
        'username': 'unauthuser',
        'email': 'unauth@example.com',
        'password_hash': 'hashedpassword'
    }), content_type='application/json')

    assert response.status_code == 401
    assert b'Unauthorized' in response.data

# Get all users with authentication
def test_get_users(test_client, access_token):
    user = User(username='testuser', email='test@example.com', password_hash='hashedpassword')
    db.session.add(user)
    db.session.commit()

    response = test_client.get('/users', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['username'] == 'testuser'
    assert data[0]['email'] == 'test@example.com'

# Get all users without authentication
def test_get_users_unauthorized(test_client):
    response = test_client.get('/users', headers={'Authorization': 'Bearer invalid_token'})
    assert response.status_code == 401
    assert b'Unauthorized' in response.data

# Update a user with authentication
def test_update_user(test_client, access_token):
    # Create a user
    user = User(username='testuser', email='test@example.com', password_hash='hashedpassword')
    db.session.add(user)
    db.session.commit()

    response = test_client.put('/users/1', data=json.dumps({
        'username': 'updateduser',
        'email': 'updated@example.com',
        'is_active': False,
        'role': 'admin'
    }), headers={'Authorization': f'Bearer {access_token}'}, content_type='application/json')

    assert response.status_code == 200
    assert b'User updated successfully' in response.data

    # Verify the update
    user = User.query.get(1)
    assert user.username == 'updateduser'
    assert user.email == 'updated@example.com'
    assert user.is_active is False
    assert user.role == 'admin'

# Update a user without authentication
def test_update_user_unauthorized(test_client):
    response = test_client.put('/users/1', data=json.dumps({
        'username': 'unauthorizedupdate',
        'email': 'unauthorized@example.com'
    }), content_type='application/json', headers={'Authorization': 'Bearer invalid_token'})

    assert response.status_code == 401
    assert b'Unauthorized' in response.data

# Update a user that does not exist
def test_update_user_not_found(test_client, access_token):
    response = test_client.put('/users/999', data=json.dumps({
        'username': 'nonexistentuser'
    }), headers={'Authorization': f'Bearer {access_token}'}, content_type='application/json')

    assert response.status_code == 404
    assert b'User not found' in response.data

# Delete a user with authentication
def test_delete_user(test_client, access_token):
    # Create a user
    user = User(username='testuser', email='test@example.com', password_hash='hashedpassword')
    db.session.add(user)
    db.session.commit()

    response = test_client.delete('/users/1', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert b'User deleted successfully' in response.data

    # Verify the deletion
    user = User.query.get(1)
    assert user is None

# Delete a user without authentication
def test_delete_user_unauthorized(test_client):
    response = test_client.delete('/users/1', headers={'Authorization': 'Bearer invalid_token'})
    assert response.status_code == 401
    assert b'Unauthorized' in response.data

# Delete a user that does not exist
def test_delete_user_not_found(test_client, access_token):
    response = test_client.delete('/users/999', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 404
    assert b'User not found' in response.data

# Create a user with missing data
def test_create_user_missing_data(test_client, access_token):
    response = test_client.post('/users', data=json.dumps({
        'username': 'incompleteuser',
        'email': 'incomplete@example.com'
        # Missing 'password_hash'
    }), headers={'Authorization': f'Bearer {access_token}'}, content_type='application/json')

    assert response.status_code == 400
    assert b'Missing required fields' in response.data

# Create a user with invalid email
def test_create_user_invalid_email(test_client, access_token):
    response = test_client.post('/users', data=json.dumps({
        'username': 'testuser',
        'email': 'invalid-email',
        'password_hash': 'hashedpassword'
    }), headers={'Authorization': f'Bearer {access_token}'}, content_type='application/json')

    assert response.status_code == 400
    assert b'Invalid email address' in response.data

# Create a user with a duplicate username
def test_create_user_duplicate_username(test_client, access_token):
    # Create a user
    test_client.post('/users', data=json.dumps({
        'username': 'duplicateuser',
        'email': 'user1@example.com',
        'password_hash': 'hashedpassword'
    }), headers={'Authorization': f'Bearer {access_token}'}, content_type='application/json')

    response = test_client.post('/users', data=json.dumps({
        'username': 'duplicateuser',
        'email': 'user2@example.com',
        'password_hash': 'hashedpassword'
    }), headers={'Authorization': f'Bearer {access_token}'}, content_type='application/json')

    assert response.status_code == 400
    assert b'Username already exists' in response.data

# Create a user with a duplicate email
def test_create_user_duplicate_email(test_client, access_token):
    # Create a user
    test_client.post('/users', data=json.dumps({
        'username': 'uniqueuser',
        'email': 'duplicate@example.com',
        'password_hash': 'hashedpassword'
    }), headers={'Authorization': f'Bearer {access_token}'}, content_type='application/json')

    response = test_client.post('/users', data=json.dumps({
        'username': 'anotheruser',
        'email': 'duplicate@example.com',
        'password_hash': 'hashedpassword'
    }), headers={'Authorization': f'Bearer {access_token}'}, content_type='application/json')

    assert response.status_code == 400
    assert b'Email already exists' in response.data
