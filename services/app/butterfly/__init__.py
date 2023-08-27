from flask import Flask
from .blueprints import register_blueprints
from .extensions.register_extensions import register_extensions
from .config.set_config import set_configuration
from .helpers.erro_handlers import register_error_handlers


def create_app(flask_env: str = 'development') -> Flask:
    app: Flask = Flask(__name__)
    set_configuration(app=app)
    register_error_handlers(app=app)
    register_extensions(app=app)
    register_blueprints(app=app)
    
    return app