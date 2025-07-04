from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler
import os 
import logging


# load env vars 
load_dotenv()

# Extensions 
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()

# create app 
def create_app():
    app = Flask(__name__)

    app.config.from_object("app.config.Config")

    # Initialize extensions 
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Register blueprints 
    from app.routes.auth import auth_bp
    from app.routes.posts import post_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(post_bp, url_prefix="/api/posts")
    
    # Logging config
    if not app.debug and not app.testing:
        handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=3)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        )
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)


    return app 

