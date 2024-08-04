from flask import Flask
from dotenv import load_dotenv
import os
from api.models.blogmodels import db
from api.config import Config, TestConfig
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity


# Load environment variables from .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__)

# Load configuration from config.py
if os.getenv('FLASK_ENV') == 'testing':
    app.config.from_object(TestConfig)
else:
    app.config.from_object(Config)

# Initialize SQLAlchemy with the app
db.init_app(app)

# Set up JWT
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')
jwt = JWTManager(app)


# Import and register blueprints
from api.routes.blogroutes import blog_bp
from api.routes.usersroutes import user_bp

app.register_blueprint(blog_bp)
app.register_blueprint(user_bp)

if __name__ == "__main__":
    app.run(debug=True)
