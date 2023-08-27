"""This module contains routes for the app."""
from flask import Blueprint, render_template, jsonify
from http import HTTPStatus

home = Blueprint("home", __name__)


@home.route("/")
@home.route("/home")
@home.route("/index")
def home_page():
    """Render the home page."""
    current_user = {'username': 'lyle'}
    return render_template("home/home.html", current_user=current_user), HTTPStatus.OK


@home.route("/like", methods=["POST"])
def like_post():
    """Like a single post."""
    return jsonify({"Resp": "greate"}), HTTPStatus.CREATED

@home.route("/likes", methods=["GET"])
def get_user_likes():
    """Get a users likes."""
    return jsonify({"Resp": "greate"}), HTTPStatus.OK

@home.route("/bookmark", methods=["POST"])
def bookmark():
    """Bookmark a single post."""
    return jsonify({"Resp": "greate"}), HTTPStatus.CREATED

@home.route("/bookmarks", methods=["GET"])
def get_user_bookmark():
    """Bookmark a single post."""
    return jsonify({"Resp": "greate"}), HTTPStatus.CREATED

@home.route("/comment", methods=["POST"])
def comment_post():
    """Comment on a single post."""
    return jsonify({"Resp": "greate"}), HTTPStatus.CREATED

@home.route("/comments", methods=["GET"])
def get_user_comments():
    """Get a posts comments."""
    return jsonify({"Resp": "greate"}), HTTPStatus.OK

@home.route("/view", methods=["POST"])
def view_post():
    """Comment on a single post."""
    return jsonify({"Resp": "greate"}), HTTPStatus.CREATED

@home.route("/views", methods=["GET"])
def get_user_views():
    """Get a posts comments."""
    return jsonify({"Resp": "greate"}), HTTPStatus.OK
