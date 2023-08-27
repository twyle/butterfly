import json

from flask import request, Flask

from ..config.logger_config import app_logger
from .rate_limiter import request_is_rate_limited
from redis import Redis
from datetime import timedelta
from http import HTTPStatus

r = Redis(host='localhost', port=6379, db=0)


def log_post_request():
    request_data = {
        "method": request.method,
        "url root": request.url_root,
        "user agent": request.user_agent,
        "scheme": request.scheme,
        "remote address": request.remote_addr,
        "headers": request.headers,
    }
    if request.args:
        request_data["args"] = request.args
    if request.form:
        request_data["data"] = request.form
    else:
        request_data["data"] = request.json
    if request.cookies:
        request_data["cookies"] = request.cookies
    if request.files:
        request_data["image"] = {
            "filename": request.files["Image"].filename,
            "content type": request.files["Image"].content_type,
            "size": len(request.files["Image"].read()) // 1000,
        }
    app_logger.info(str(request_data))


def log_get_request():
    request_data = {
        "method": request.method,
        "url root": request.url_root,
        "user agent": request.user_agent,
        "scheme": request.scheme,
        "remote address": request.remote_addr,
        "headers": request.headers,
        "route": request.endpoint,
        "base url": request.base_url,
        "url": request.url,
    }
    if request.args:
        request_data["args"] = request.args
    if request.cookies:
        request_data["cookies"] = request.cookies
    app_logger.info(str(request_data))


def get_response(response):
    response_data = {
        "status": response.status,
        "status code": response.status_code,
        "response": json.loads(response.data),
    }
    app_logger.info(str(response_data))


def get_exception(exc):
    """Log exceptions"""
    if exc:
        app_logger.warning(f"{exc.__class__.__name__ }: {str(exc)}")
        
        
def register_app_hooks(app: Flask):
    @app.before_first_request
    def application_startup():
        """Log the beginning of the application."""
        app_logger.info('Web app is up!')

    @app.before_request
    def log_request():
        """Log the data held in the request"""
        if request.method in ['POST', 'PUT']:
            log_post_request()
        elif request.method in ['GET', 'DELETE']:
            log_get_request()

    @app.after_request
    def log_response(response):
        try:
            get_response(response)
        except Exception:
            pass
        finally:
            return response

    @app.teardown_request
    def log_exception(exc):
        get_exception(exc)
        
    # @app.before_request
    # def rate_limit_request():
    #     if request_is_rate_limited(r, 'admin', 10, timedelta(seconds=60)):
    #         return {'Error': 'You have exceeded the allowed requests'}, HTTPStatus.TOO_MANY_REQUESTS