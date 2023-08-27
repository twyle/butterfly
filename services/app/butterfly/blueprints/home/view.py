"""This module contains routes for the app."""
from flask import Blueprint, render_template, jsonify, request
from http import HTTPStatus
from ..database.schemas.activity import ActivityCreated, CreateActivity
from ..database.models import (
    User, Post, Comment, Bookmark, Like, View
)
from ..database.schemas.user import GetUser
from ..database.schemas.post import GetPost
from ..database.database import get_db
from ..database.crud.user import get_user
from ..database.crud.post import get_post
from ..database.crud.bookmark import (
    create_bookmark, delete_bookmark, list_user_bookmarks, has_bookmarked
)
from pydantic import ValidationError
from sqlalchemy.exc import OperationalError, IntegrityError


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
    try:
        bookmark_data = CreateActivity(**request.args)
    except ValidationError:
        return {'Error': 'The data provided is invalid or incomplete!'}, HTTPStatus.BAD_REQUEST
    user_data = GetUser(user_id=bookmark_data.user_id)
    user: User = get_user(session=get_db, user_data=user_data)
    if not user:
        return {'Error': f'User with id {user_data.user_id} does not exists'}, HTTPStatus.NOT_FOUND 
    post_data = GetPost(post_id=bookmark_data.post_id)
    post: Post = get_post(session=get_db, post_data=post_data)
    if not post:
        return {'Error': f'post with id {post_data.post_id} does not exists'}, HTTPStatus.NOT_FOUND
    try:
        if has_bookmarked(session=get_db, activity=bookmark_data):
            return {'Error': f'The user with id {bookmark_data.user_id} has already bookmarked article with id {bookmark_data.post_id}'}, HTTPStatus.CONFLICT
        bookmark: Bookmark = create_bookmark(session=get_db, activity=bookmark_data)
    except (OperationalError, IntegrityError) as e:
        print(e)
        # Send email to
        return {'Error': 'The application is experiencing a tempoary error. Please try again in a few minutes.'}, HTTPStatus.INTERNAL_SERVER_ERROR
    resp = ActivityCreated(
        user_id=bookmark.author_id,
        post_id=bookmark.post_id,
        date_created=bookmark.bookmark_date
    ).model_dump_json(indent=4)
    return resp, HTTPStatus.CREATED


@home.route("/bookmarks", methods=["GET"])
def get_user_bookmark():
    """Bookmark a single post."""
    try:
        user_data = GetUser(user_id=request.args.get('user_id'))
    except ValidationError:
        return {'error': 'Invalid input: you probably did not include the user id.'}, HTTPStatus.BAD_REQUEST
    try:
        user = get_user(session=get_db, user_data=user_data)
        if not user:
            return {'Error': f'User with id {user_data.user_id} does not exists'}, HTTPStatus.NOT_FOUND
        bookmarks: list[Bookmark] = list_user_bookmarks(session=get_db, user_data=user_data)
    except (OperationalError, IntegrityError) as e:
        print(e)
        # Send email to
        return {'Error': 'The application is experiencing a tempoary error. Please try again in a few minutes.'}, HTTPStatus.INTERNAL_SERVER_ERROR
    resp = [
        ActivityCreated(
            user_id=bookmark.author_id,
            post_id=bookmark.post_id,
            date_created=bookmark.bookmark_date
        ).model_dump()
        for bookmark in bookmarks
    ]
    return resp, HTTPStatus.OK


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
