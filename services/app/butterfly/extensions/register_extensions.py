"""This module resgisters the application extensions.

Example:
    To register the extensions:
        register_extensions(app)

@Author: Lyle Okoth
@Date: 28/06/2023
@Portfolio: https://lyleokoth.oryks-sytem.com
"""
from flask import Flask

from .extensions import bcrypt, cors


def register_extensions(app: Flask) -> None:
    """Register the application extensions.

    Parameters
    ----------
    app: flask.Flask
        The Flask app instance.
    """
    bcrypt.init_app(app)
    cors.init_app(app)
