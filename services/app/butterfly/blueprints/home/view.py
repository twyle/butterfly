"""This module contains routes for the app."""
from flask import Blueprint, render_template
from http import HTTPStatus

home = Blueprint("home", __name__)


@home.route("/")
@home.route("/home")
@home.route("/index")
def home_page():
    """Render the home page."""
    current_user = {'username': 'lyle'}
    return render_template("home/home.html", current_user=current_user), HTTPStatus.OK
