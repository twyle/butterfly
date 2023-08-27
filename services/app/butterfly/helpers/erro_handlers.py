# -*- coding: utf-8 -*-
"""This module declares the error handlers and the error handlers register functions.

Example:
    To register the error handlers:
        register_error_handlers(app)

@Author: Lyle Okoth
@Date: 28/06/2023
@Portfolio: https://lyleokoth.oryks-sytem.com
"""
from http import HTTPStatus

from flask import Flask, Response, jsonify, make_response


def handle_resource_not_found(exeption: Exception) -> Response:
    """Handle all resource not found errors.

    Called when an requested resource is not found on the server.

    Parameters
    ----------
    exception: Exception
        The exception that was raised. This is a subclass of Exception.

    Returns
    -------
    Response:
        A string consiting of json data and response code.
    """
    return make_response(jsonify({"error": str(exeption)}), HTTPStatus.NOT_FOUND)


def handle_method_not_allowed(exeption: Exception) -> Response:
    """Handle all method not allowed errors.

    Called when a route tries to handle a request with a methods that is not
    allowed for the given route.

    Parameters
    ----------
    exception: Exception
        The exception that was raised. This is a subclass of Exception.

    Returns
    -------
    Response:
        A string consiting of json data and response code.
    """
    return make_response(jsonify({"error": str(exeption)}), HTTPStatus.METHOD_NOT_ALLOWED)


def handle_internal_server_error(exeption: Exception) -> Response:
    """Handle all internal server errors.

    This method is called when an error occurs within the application server.

    Parameters
    ----------
    exception: Exception
        The exception that was raised. This is a subclass of Exception.

    Returns
    -------
    Response:
        A string consiting of json data and response code.
    """
    return make_response(jsonify({"error": str(exeption)}), HTTPStatus.INTERNAL_SERVER_ERROR)


def handle_unsupported_media_type(exeption: Exception) -> Response:
    """Handle all unsupported media type errors.

    This method is called when a a request does not supply the data or the data supplied is
    invalid.

    Parameters
    ----------
    exception: Exception
        The exception that was raised. This is a subclass of Exception.

    Returns
    -------
    Response:
        A string consiting of json data and response code.
    """
    return make_response(jsonify({"error": str(exeption)}), HTTPStatus.UNSUPPORTED_MEDIA_TYPE)


def register_error_handlers(app: Flask) -> None:
    """Register the error handlers.

    Parameters
    ----------
    app: flask.Flask
        The Flask app instance.
    """
    app.register_error_handler(HTTPStatus.NOT_FOUND, handle_resource_not_found)
    app.register_error_handler(HTTPStatus.METHOD_NOT_ALLOWED, handle_method_not_allowed)
    app.register_error_handler(HTTPStatus.INTERNAL_SERVER_ERROR, handle_internal_server_error)
    app.register_error_handler(HTTPStatus.UNSUPPORTED_MEDIA_TYPE, handle_unsupported_media_type)