from flask import request, Blueprint, jsonify
from api.models.blogmodels import db, BlogPost, User
from flask_jwt_extended import jwt_required


blog_bp = Blueprint('blog', __name__, url_prefix='/api/v1')

@blog_bp.route('/blog_posts', methods=['POST'])
def create_blog_post():
  
    data = request.get_json()
    try:
        title = data.get('title')
        content = data.get('content')
        author_id = data.get('author_id')

        if not title or not content or not author_id:
            return jsonify({'message': 'Missing required fields'}), 400

        author = User.query.get(author_id)
        if not author:
            return jsonify({'message': 'Author not found'}), 404

        new_post = BlogPost(title=title, content=content, author_id=author_id)
        db.session.add(new_post)
        db.session.commit()

        return jsonify({
            'id': str(new_post.id),
            'title': new_post.title,
            'content': new_post.content,
            'author_id': str(new_post.author_id),
            'created_at': new_post.created_at
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
