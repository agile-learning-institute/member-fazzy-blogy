import uuid
from flask import Flask, request, jsonify, Blueprint
from api.models.blogmodels import User
from werkzeug.security import generate_password_hash

user_bp = Blueprint('users', __name__, url_prefix='/api/v1')

# Create user
@user_bp.route('/users', methods=['POST'])
def create_user():
    from api.models.blogmodels import db
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    role = data.get('role', 'user')

    # Validate required fields
    if not username or not email or not password or not firstname or not lastname:
        return jsonify({'error': 'Missing required fields'}), 400

    # Check for valid email
    if '@' not in email:
        return jsonify({'message': 'Invalid email address'}), 400

    # Check if username or email already exists
    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return jsonify({'error': 'User with that username or email already exists'}), 409

    # Hash the password
    hashed_password = generate_password_hash(password)

    # Create a new user
    new_user = User(
        id=uuid.uuid4(),
        username=username,
        email=email,
        password=hashed_password,
        firstname=firstname,
        lastname=lastname,
        role=role
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'message': 'User created successfully',
        'id': new_user.id,
        'username': new_user.username,
        'email': new_user.email,
        'firstname': new_user.firstname,
        'lastname': new_user.lastname,
        'role': new_user.role,
        'created_at': new_user.created_at
    }), 201


# @user_bp.route('/users', methods=['GET'])
# def get_users():
#     users = User.query.all()
#     users_list = [
#         {
#             'id': user.id,
#             'username': user.username,
#             'email': user.email,
#             'is_active': user.is_active,
#             'role': user.role
#         } for user in users
#     ]
#     return jsonify(users_list), 200

# @user_bp.route('/users/<int:user_id>', methods=['PUT'])
# def update_user(user_id):
#     from api.models.blogmodels import db
#     data = request.json
#     user = User.query.get(user_id)

#     if user:
#         user.username = data.get('username', user.username)
#         user.email = data.get('email', user.email)
#         user.is_active = data.get('is_active', user.is_active)
#         user.role = data.get('role', user.role)
#         db.session.commit()
#         return jsonify({'message': 'User updated successfully'}), 200
#     else:
#         return jsonify({'message': 'User not found'}), 404

# @user_bp.route('/users/<int:user_id>', methods=['DELETE'])
# def delete_user(user_id):
#     from api.models.blogmodels import db
#     user = User.query.get(user_id)

#     if user:
#         db.session.delete(user)
#         db.session.commit()
#         return jsonify({'message': 'User deleted successfully'}), 200
#     else:
#         return jsonify({'message': 'User not found'}), 404
# app = Flask(__name__)