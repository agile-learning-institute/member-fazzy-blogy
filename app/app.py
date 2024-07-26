from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from routes.blogroutes import bp as blog_bp
from config import Config

app = Flask(__name__)
app.config.from_config(config)

db = SQLAlchemy(app)

# Register Blueprints
app.register_blueprint(blog_bp)

# @app.route('/')
# def index():
#     return '''
#     <!DOCTYPE html>
#     <html lang="en">
#       <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <title>Home</title>
#       </head>
#       <body>
#         <h1>Welcome to the Home Page</h1>
#         <p>This is the main index page.</p>
#       </body>
#     </html>
#     '''

if __name__ == '__main__':
    app.run(debug=True)
