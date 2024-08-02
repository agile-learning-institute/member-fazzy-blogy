from flask import Flask
from dotenv import load_dotenv
import os
from api.models.blogmodels import db, User, BlogPost, Comment

# Load environment variables from .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__)

# Load configuration from config.py
if os.getenv('FLASK_ENV') == 'testing':
    app.config.from_object('config.TestConfig')
else:
    app.config.from_object('config.Config')

# Initialize SQLAlchemy with the app
db.init_app(app)

# Import and register blueprints
from api.routes.blogroutes import blog_bp
from api.routes.usersroutes import user_bp

app.register_blueprint(blog_bp)
app.register_blueprint(user_bp)

if __name__ == "__main__":
    app.run(debug=True)
