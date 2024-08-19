from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.models.blogmodels import db, BlogPost, User, Comment
from api.schemas.blogschema import BlogPostSchema
from sqlalchemy.exc import SQLAlchemyError

blog_post_schema = BlogPostSchema()


blog_bp = Blueprint('blog', __name__, url_prefix='/api/v1')

# Create a blog post
@blog_bp.route('/blog_posts', methods=['POST'])
@jwt_required()
def create_blog_post():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    author_id = data.get('author_id')

    if not title or not content or not author_id:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        user = User.query.get(author_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        new_post = BlogPost(title=title, content=content, author_id=author_id)
        db.session.add(new_post)
        db.session.commit()
        return jsonify({'message': 'Blog post created successfully', 'post': {
            'id': str(new_post.id),
            'title': new_post.title,
            'content': new_post.content,
            'author_id': str(new_post.author_id)
        }}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Route to fetch all blog posts with pagination and authentication
@blog_bp.route('/blog_posts', methods=['GET'])
# @jwt_required()
def get_blog_posts():
    from api.app import app
    try:
        # Pagination parameters
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        # Validate pagination parameters
        if page < 1 or per_page < 1:
            return jsonify({'error': 'Invalid pagination parameters'}), 400

        # Fetch paginated blog posts
        paginated_posts = BlogPost.query.paginate(page=page, per_page=per_page, error_out=False)
        posts_schema = BlogPostSchema(many=True)
        result = posts_schema.dump(paginated_posts.items)

        # Add pagination metadata to response
        response = {
            'posts': result,
            'total': paginated_posts.total,
            'pages': paginated_posts.pages,
            'current_page': paginated_posts.page,
            'next_page': paginated_posts.next_num if paginated_posts.has_next else None,
            'prev_page': paginated_posts.prev_num if paginated_posts.has_prev else None
        }

        return jsonify(response), 200

    except SQLAlchemyError as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({'error': 'Database error occurred'}), 500

    except Exception as e:
        app.logger.error(f"Internal server error: {e}")
        return jsonify({'error': 'Internal server error'}), 500



# Get a blog post
@blog_bp.route('/blog_posts/<string:post_id>', methods=['GET'])
@jwt_required()
def get_blog_post(post_id):
    from api.app import app
    try:
        post = BlogPost.query.get_or_404(post_id)

        post_data = blog_post_schema.dump(post)

        return jsonify(post_data), 200

    except SQLAlchemyError as e:
        app.loggger.error(f"Database error: {e}")
        return jsonify({'error': 'Database error occurred'}), 500

    except Exception as e:
        app.loggger.error(f"Internal server error: {e}")
        return jsonify({'error': 'Internal server error occurred'}), 500


# Update a blog post
@blog_bp.route('/blog_posts/<string:post_id>', methods=['PUT'])
@jwt_required()
def update_blog_post(post_id):
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    if not title and not content:
        return jsonify({'error': 'Missing fields to update'}), 400

    try:
        with db.session.begin_nested():
            post = BlogPost.query.get_or_404(post_id)
            if title:
                post.title = title
            if content:
                post.content = content

            db.session.commit()

        return jsonify({
            'message': 'Blog post updated successfully',
            'post': {
                'id': str(post.id),
                'title': post.title,
                'content': post.content
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500



# Delete a blog post
@blog_bp.route('/blog_posts/<string:post_id>', methods=['DELETE'])
# @jwt_required()
def delete_blog_post(post_id):
    from api.app import app
    try:
        with db.session.begin_nested():
            post = BlogPost.query.get_or_404(post_id)
            db.session.delete(post)
            db.session.commit()

        return jsonify({'message': 'Blog post deleted successfully'}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        app.logger.error(f"Database error occurred while deleting blog post: {e}")
        return jsonify({'error': 'A database error occurred'}), 500

    except Exception as e:
        app.logger.error(f"An unexpected error occurred: {e}")
        return jsonify({'error': 'Internal server error'}), 500

