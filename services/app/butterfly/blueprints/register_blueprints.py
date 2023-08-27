"""This module registers the application blueprints.

Example:
    To register the blueprints:
        register_blueprints(app)

@Author: Lyle Okoth
@Date: 28/06/2023
@Portfolio: https://lyleokoth.oryks-sytem.com
"""

from flask import Flask

from .home.view import home
from .auth.view import auth
from .post.view import post

def register_blueprints(app: Flask) -> None:
    """Register the application blueprints.

    Parameters
    ----------
    app: flask.Flask
        The Flask app instance.
    """
    app.register_blueprint(home, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(post, url_prefix="/post")
