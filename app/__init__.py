from flask import Flask, render_template, url_for
from config import DevelopmentConfig

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)


    # import blueprints
    from app.blueprints.auth.auth_routes import auth_bp
    # register blueprints
    app.register_blueprint(auth_bp)
    
    return app