from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os 


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
    app.register_blueprint(post_bp, url_prefix="api/posts")

    return app 

