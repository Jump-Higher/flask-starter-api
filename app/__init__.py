from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Db_config, Cloudinary_config, Mail_config
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.prefix_middleware import PrefixMiddleware
from flask_mail import Mail
import os
from app.hash import hash_password

# Create Flask app
app = Flask(__name__)

# Load config from object
app.config.from_object(Cloudinary_config)
app.config.from_object(Db_config)
app.config.from_object(Mail_config)

# Set secret key for email verification
secret_key = app.config['SECRET_KEY'] = os.getenv('EMAIL_SECRET_KEY')

# Initialize database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize mail sending
mail_config = Mail_config
mail = Mail(app)

# Adding CORS
CORS(app)

# Setup jwt config
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

# URL prefix
app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix='/starter-api/v1')

# Create Super Admin
from app.super_admin import create_superadmin
create_superadmin()

from app import routes
if __name__ == "__main__":
    app.run()