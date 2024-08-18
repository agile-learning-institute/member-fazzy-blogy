import uuid
from uuid import UUID
from flask import request, jsonify, Blueprint
from api.models.blogmodels import User
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, create_access_token
from api.schemas.userschema import UserSchema


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



# Route to get users with pagination and authentication
user_schema = UserSchema(many=True)
@user_bp.route('/users', methods=['GET'])
# @jwt_required()
def get_users():
    try:
        # Pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        if page < 1 or per_page < 1:
            return jsonify({'error': 'Invalid pagination parameters'}), 400

        # Fetch users with pagination
        users = User.query.paginate(page=page, per_page=per_page, error_out=False)
        result = user_schema.dump(users.items)  # Use schema to dump data

        # Add pagination metadata
        response = {
            'users': result,
            'total': users.total,
            'pages': users.pages,
            'current_page': users.page,
            'next_page': users.next_num if users.has_next else None,
            'prev_page': users.prev_num if users.has_prev else None
        }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# get a user
@user_bp.route('/users/<string:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    try:
        user = User.query.get_or_404(user_id)

        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'firstname': user.firstname,
            'lastname': user.lastname,
            'role': user.role,
            'created_at': user.created_at
        }

        return jsonify(user_data), 200

    except SQLAlchemyError as e:
        return jsonify({'error': 'Database error occurred'}), 500

    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500


# update user
@user_bp.route('/users/<string:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    from api.models.blogmodels import db
    try:
        user_id = UUID(user_id, version=4)
    except ValueError:
        return jsonify({"msg": "Invalid user ID format"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"msg": "No input data provided"}), 400

    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    user.is_active = data.get('is_active', user.is_active)
    user.role = data.get('role', user.role)

    db.session.commit()

    return jsonify({
        'id': str(user.id),
        'username': user.username,
        'email': user.email,
        'is_active': user.is_active,
        'role': user.role
    }), 200

# Delete a user
@user_bp.route('/users/<string:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    from api.models.blogmodels import db
    from api.app import app
    try:
        user = User.query.get(user_id)

        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'message': 'User deleted successfully'}), 200
        else:
            return jsonify({'message': 'User not found'}), 404

    except SQLAlchemyError as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({'error': 'Database error occurred'}), 500

    except Exception as e:
        app.logger.error(f"Internal server error: {e}")
        return jsonify({'error': 'Internal server error'}), 500


# Route for creating an access token for testing purposes
@user_bp.route('/login', methods=['POST'])
def login():
    from api.app import app
    data = request.get_json()
    app.logger.info(f"Received login data: {data}")

    identifier = data.get('identifier')
    password = data.get('password')

    if not identifier or not password:
        return jsonify({'message': 'Missing required fields'}), 400

    user = User.query.filter((User.username == identifier) | (User.email == identifier)).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=user.username)
        return jsonify(access_token=access_token, message='Login successful'), 200
    else:
        return jsonify({'message': 'Invalid username/email or password'}), 401
