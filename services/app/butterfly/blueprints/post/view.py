"""This module contains routes for the app."""
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from http import HTTPStatus
from ..database.schemas.post import (
    CreatePost, CreatedPost, GetPost, GetPosts, UpdatePost
)
from ..database.crud.post import (
    create_post, get_post, get_posts, delete_post, update_post
)
from ..database.models.post import Post
from ..database.database import get_db
from pydantic import ValidationError
from sqlalchemy.exc import OperationalError, IntegrityError
from ..database.models.user import User
from ..database.crud.user import get_user
from ..database.schemas.user import GetUser

post = Blueprint("post", __name__)

 
@post.route("/create", methods=["POST", "GET"])
def create_new_post():
    """Create a new post."""
    if request.method == 'GET':
        return {'success': 'post creation form'}, HTTPStatus.OK
    elif request.method == 'POST':
        try:
            post_data = CreatePost(**request.form) 
        except ValidationError:
            return {'Error': 'The data provided is invalid or incomplete!'}, HTTPStatus.BAD_REQUEST
        try:
            user_data = GetUser(user_id=post_data.author_id)
            user = get_user(session=get_db, user_data=user_data)
            if not user:
                return {'Error': f'User with id {user_data.user_id} does not exists'}, HTTPStatus.NOT_FOUND 
            post: Post = create_post(post_data=post_data, post_image=request.files, session=get_db) 
        except (OperationalError, IntegrityError) as e:
            print(e)
            # Send email to
            return {'Error': 'The application is experiencing a tempoary error. Please try again in a few minutes.'}, HTTPStatus.INTERNAL_SERVER_ERROR
        resp = CreatedPost(
            id=post.id,
            location=post.location,
            text=post.text,
            image_url=post.image_url,
            author_id=post.author_id,
            date_published=post.date_published
        )
        return resp.model_dump_json(indent=4), HTTPStatus.CREATED


@post.route("/update", methods=["PUT"])
def update_one_post():
    """Update a post."""
    if request.method == 'GET':
        return {'success': 'post creation form'}, HTTPStatus.OK
    elif request.method == 'PUT':
        try:
            post_data = UpdatePost(
                **request.form
            )
        except ValidationError:
            return {'Error': 'The data provided is invalid or incomplete!'}, HTTPStatus.BAD_REQUEST
        try:
            user_data = GetUser(user_id=post_data.author_id)
            user: User = get_user(session=get_db, user_data=user_data)
            if not user:
                return {'Error': f'User with id {user_data.user_id} does not exists'}, HTTPStatus.NOT_FOUND 
            post: Post = get_post(session=get_db, post_data=post_data)
            if not post:
                return {'Error': f'post with id {post_data.post_id} does not exists'}, HTTPStatus.NOT_FOUND
            if user.id != post.author_id:
                return {'Error': 'You can only update your own post!'}, HTTPStatus.FORBIDDEN
            post: Post = update_post(post_data=post_data, post_image=request.files, session=get_db) 
        except (OperationalError, IntegrityError) as e:
            print(e)
            # Send email to
            return {'Error': 'The application is experiencing a tempoary error. Please try again in a few minutes.'}, HTTPStatus.INTERNAL_SERVER_ERROR
        resp = CreatedPost(
            id=post.id,
            location=post.location,
            text=post.text,
            image_url=post.image_url,
            author_id=post.author_id,
            date_published=post.date_published
        )
        return resp.model_dump_json(indent=4), HTTPStatus.CREATED


@post.route("/delete", methods=["DELETE"])
def delete_one_post():
    """Delete a post."""
    try:
        post_data = GetPost(post_id=request.args.get('post_id'))
    except ValidationError:
        return {'error': 'Invalid input: you probably did not include the post id.'}, HTTPStatus.BAD_REQUEST
    try:
        post = get_post(session=get_db, post_data=post_data)
        if not post:
            return {'Error': f'post with id {post_data.post_id} does not exists'}, HTTPStatus.NOT_FOUND
        post = delete_post(get_db, GetPost(post_id=request.args.get('post_id')))
    except (OperationalError, IntegrityError) as e:
        print(e)
        # Send email to
        return {'Error': 'The application is experiencing a tempoary error. Please try again in a few minutes.'}, HTTPStatus.INTERNAL_SERVER_ERROR
    resp = CreatedPost(
            id=post.id,
            location=post.location,
            text=post.text,
            image_url=post.image_url,
            author_id=post.author_id,
            date_published=post.date_published
        )
    return resp.model_dump_json(indent=4), HTTPStatus.OK


@post.route("/get", methods=["GET"])
def get_one_post():
    """Get a single post."""
    try:
        post_data = GetPost(post_id=request.args.get('post_id'))
    except ValidationError:
        return {'error': 'Invalid input: you probably did not include the post id.'}, HTTPStatus.BAD_REQUEST
    try:
        post = get_post(session=get_db, post_data=post_data)
    except (OperationalError, IntegrityError) as e:
        print(e)
        # Send email to
        return {'Error': 'The application is experiencing a tempoary error. Please try again in a few minutes.'}, HTTPStatus.INTERNAL_SERVER_ERROR
    if post:
        resp = CreatedPost(
            id=post.id,
            location=post.location,
            text=post.text,
            image_url=post.image_url,
            author_id=post.author_id,
            date_published=post.date_published
        )
        return resp.model_dump_json(indent=4), HTTPStatus.OK
    
    return {'Error':f'No post with id {post_data.post_id}'}, HTTPStatus.NOT_FOUND


@post.route("/posts", methods=["GET"])
def get_all_posts():
    """Get many post post."""
    offset: str = request.args.get('offset')
    limit: str = request.args.get('limit')
    try:
        posts = get_posts(get_db, GetPosts(offset=offset, limit=limit))
    except (OperationalError, IntegrityError) as e:
            print(e)
            # Send email to
            return {'Error': 'The application is experiencing a tempoary error. Please try again in a few minutes.'}, HTTPStatus.INTERNAL_SERVER_ERROR
    posts = [
        CreatedPost(
            id=post.id,
            location=post.location,
            text=post.text,
            image_url=post.image_url,
            author_id=post.author_id,
            date_published=post.date_published
        ).model_dump()
        for post in posts
    ]
    return posts, HTTPStatus.OK



@post.route("/likes", methods=["GET"])
def get_post_likes():
    """Get a posts likes."""
    return jsonify({"Resp": "greate"}), HTTPStatus.OK


@post.route("/bookmark", methods=["GET"])
def get_post_bookmarks():
    """Bookmark a single post."""
    return jsonify({"Resp": "greate"}), HTTPStatus.CREATED


@post.route("/comments", methods=["GET"])
def get_post_comments():
    """Get a posts comments."""
    return jsonify({"Resp": "greate"}), HTTPStatus.OK


@post.route("/views", methods=["GET"])
def get_post_views():
    """Get a posts comments."""
    return jsonify({"Resp": "greate"}), HTTPStatus.OK
