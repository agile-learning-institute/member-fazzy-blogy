from flask import Flask, request, jsonify, Blueprint
from api.models.blogmodels import User
from werkzeug.security import generate_password_hash



user_bp = Blueprint('users', __name__, url_prefix='/api/v1')


@user_bp.route('/users', methods=['POST'])
def create_user():
    from api.models.blogmodels import db
    data = request.json

    # Validate required fields
    if not all(field in data for field in ('username', 'email', 'password')):
        return jsonify({'message': 'Missing required fields'}), 400

    # Check for valid email
    if '@' not in data['email']:
        return jsonify({'message': 'Invalid email address'}), 400

    # Check if username or email already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already exists'}), 400

    # Hash the password
    hashed_password = generate_password_hash(data['password'])

    # Create a new user
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201


@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = [
        {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_active': user.is_active,
            'role': user.role
        } for user in users
    ]
    return jsonify(users_list), 200

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    from api.models.blogmodels import db
    data = request.json
    user = User.query.get(user_id)

    if user:
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.is_active = data.get('is_active', user.is_active)
        user.role = data.get('role', user.role)
        db.session.commit()
        return jsonify({'message': 'User updated successfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    from api.models.blogmodels import db
    user = User.query.get(user_id)

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404
app = Flask(__name__)