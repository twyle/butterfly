"""This script contains helper methods for use with the application."""
from flask import Flask

from .config import Config


def set_configuration(app: Flask, flask_env: str = "development") -> None:
    """Set the application configuration.

    The application configuration will depend on the
    environment i.e Test, Development, Staging or Production.

    Parameters
    ----------
    app: flask.Flask
        A flask app instance.
    """
    app.config.from_object(Config[flask_env])
