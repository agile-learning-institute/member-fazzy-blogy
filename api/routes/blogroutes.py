from flask import Blueprint, jsonify

blog_bp = Blueprint('blog', __name__, url_prefix='/api/v1')

@blog_bp.route('/', methods=['GET'])
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>API v1</title>
      </head>
      <body>
        <h1>Welcome to API v1</h1>
        <p>This is a simple API version 1.</p>
      </body>
    </html>
    '''

@blog_bp.route('/hello', methods=['GET'])
def api():
    return jsonify({"message": "Hello from API v1!"})
