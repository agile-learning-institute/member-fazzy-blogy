
from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from api.schemas.commentshema import comment_schema
from api.models.blogmodels import BlogPost, User, Comment, db
from sqlalchemy.exc import SQLAlchemyError


comments_bp = Blueprint('comments', __name__, url_prefix='/api/v1')

# create comment


@comments_bp.route('/comments', methods=['POST'])
@jwt_required()
def create_comment():
    data = request.get_json()
    blog_post_id = data.get('blog_post_id')
    user_id = data.get('user_id')
    comment_text = data.get('comment')

    if not blog_post_id or not user_id or not comment_text:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        post = BlogPost.query.get(blog_post_id)
        user = User.query.get(user_id)

        if not post:
            return jsonify({'error': 'Blog post not found'}), 404
        if not user:
            return jsonify({'error': 'User not found'}), 404

        new_comment = Comment(blog_post_id=blog_post_id,
                              user_id=user_id, comment=comment_text)
        db.session.add(new_comment)
        db.session.commit()
        return jsonify({'message': 'Comment added successfully', 'comment': {
            'id': str(new_comment.id),
            'blog_post_id': str(new_comment.blog_post_id),
            'user_id': str(new_comment.user_id),
            'comment': new_comment.comment,
            'created_at': new_comment.created_at
        }}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred', 'details': str(e)}), 500

# get comments


@comments_bp.route('/blog_posts/<string:post_id>/comments', methods=['GET'])
@jwt_required()
def get_comments_for_blog_post(post_id):
    try:
        post = BlogPost.query.get_or_404(post_id)

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        if page < 1 or per_page < 1:
            return jsonify({'error': 'Page number and per_page must be positive integers'}), 400

        pagination = Comment.query.filter_by(blog_post_id=post.id).paginate(page=page, per_page=per_page, error_out=False)

        comments_data = [{
            'id': str(comment.id),
            'user_id': str(comment.user_id),
            'comment': comment.comment,
            'created_at': comment.created_at
        } for comment in pagination.items]

        result = {
            'post_id': str(post.id),
            'comments': comments_data,
            'page': page,
            'per_page': per_page,
            'total_comments': pagination.total,
            'total_pages': pagination.pages
        }

        return jsonify(result), 200
    except SQLAlchemyError as e:
        return jsonify({'error': 'Database error occurred', 'details': str(e)}), 500

# get a comment
@comments_bp.route('/comments/<string:comment_id>', methods=['GET'])
@jwt_required()
def get_comment(comment_id):
    from api.app import app
    if not comment_id:
        return jsonify({'error': 'Invalid comment ID format'}), 400

    try:
        comment = Comment.query.get_or_404(comment_id)

        comment_data = {
            'id': str(comment.id),
            'blog_post_id': str(comment.blog_post_id),
            'user_id': str(comment.user_id),
            'comment': comment.comment,
            'created_at': comment.created_at
        }

        return jsonify(comment_data), 200
    except SQLAlchemyError as e:
        app.logger.error(f"Database error occurred: {str(e)}")
        return jsonify({'error': 'Database error occurred', 'details': str(e)}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500

# update a comment
# delete a comment
