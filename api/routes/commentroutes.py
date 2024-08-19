
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

        new_comment = Comment(blog_post_id=blog_post_id, user_id=user_id, comment=comment_text)
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
# get a comment
# update a comment
# delete a comment