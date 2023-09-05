"""This module contains routes for the app."""
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from http import HTTPStatus
from ..database.schemas.post import (
    CreatePost, CreatedPost, GetPost, GetPosts, UpdatePost, PostSchema, PostAuthor
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
from ..database.models.bookmark import Bookmark
from ..database.crud.bookmark import list_post_bookmarks
from ..database.schemas.activity import ActivityCreated, RepeatableActivityCreated, CommentCreated
from ..database.crud.like import list_post_likes
from ..database.models.like import Like
from ..database.models.comment import Comment
from ..database.models.view import View
from ..database.crud.view import (
    list_post_views
)
from ..database.crud.comment import list_post_comments
from ..home.helpers import load_posts

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
    created_posts = []
    for post in posts:
        post_author: PostAuthor = PostAuthor(
            id=post.author.id,
            profile_picture=url_for('static', filename='img/default.jpeg'),
            name=post.author.first_name
        )
        post_schema: PostSchema = PostSchema(
            id=post.id,
            text=post.text,
            image=url_for('static', filename=f'img/{post.image_url}'),
            location=post.location,
            date_published='10',
            author=post_author
        ).model_dump()
        created_posts.append(post_schema)
    # posts = [
    #     CreatedPost(
    #         id=post.id,
    #         location=post.location,
    #         text=post.text,
    #         image_url=post.image_url,
    #         author_id=post.author_id,
    #         date_published=post.date_published
    #     ).model_dump()
    #     for post in posts
    # ]
    return created_posts, HTTPStatus.OK

@post.route("/load_more_posts", methods=["GET"])
def load_more_posts():
    """Get a single post."""
    offset: str = request.args.get('offset', 0)
    limit: str = request.args.get('limit', 10)
    more_posts = load_posts(limit=int(limit), offset=int(offset))
    return more_posts

@post.route("/likes", methods=["GET"])
def get_post_likes():
    """Get a posts likes."""
    try:
        post_data = GetPost(post_id=request.args.get('post_id'))
    except ValidationError:
        return {'error': 'Invalid input: you probably did not include the post id.'}, HTTPStatus.BAD_REQUEST
    try:
        post: Post = get_post(session=get_db, post_data=post_data)
        if not post:
            return {'Error': f'post with id {post_data.post_id} does not exists'}, HTTPStatus.NOT_FOUND
        likes: list[Bookmark] = list_post_likes(session=get_db, post_data=post_data)
    except (OperationalError, IntegrityError) as e:
        print(e)
        # Send email to
        return {'Error': 'The application is experiencing a tempoary error. Please try again in a few minutes.'}, HTTPStatus.INTERNAL_SERVER_ERROR
    resp = [
        ActivityCreated(
            user_id=like.author_id,
            post_id=like.post_id,
            date_created=like.like_date
        ).model_dump()
        for like in likes
    ]
    return resp, HTTPStatus.OK


@post.route("/bookmarks", methods=["GET"])
def get_post_bookmarks():
    """Bookmark a single post."""
    try:
        post_data = GetPost(post_id=request.args.get('post_id'))
    except ValidationError:
        return {'error': 'Invalid input: you probably did not include the post id.'}, HTTPStatus.BAD_REQUEST
    try:
        post: Post = get_post(session=get_db, post_data=post_data)
        if not post:
            return {'Error': f'post with id {post_data.post_id} does not exists'}, HTTPStatus.NOT_FOUND
        bookmarks: list[Bookmark] = list_post_bookmarks(session=get_db, post_data=post_data)
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


@post.route("/comments", methods=["GET"])
def get_post_comments():
    """Get a posts comments."""
    try:
        post_data = GetPost(post_id=request.args.get('post_id'))
    except ValidationError:
        return {'error': 'Invalid input: you probably did not include the post id.'}, HTTPStatus.BAD_REQUEST
    try:
        post: Post = get_post(session=get_db, post_data=post_data)
        if not post:
            return {'Error': f'post with id {post_data.post_id} does not exists'}, HTTPStatus.NOT_FOUND
        comments: list[Comment] = list_post_comments(session=get_db, post_data=post_data)
    except (OperationalError, IntegrityError) as e:
        print(e)
        # Send email to
        return {'Error': 'The application is experiencing a tempoary error. Please try again in a few minutes.'}, HTTPStatus.INTERNAL_SERVER_ERROR
    resp = [
        CommentCreated(
            user_id=comment.author_id,
            post_id=comment.post_id,
            date_created=comment.comment_date,
            comment_id=comment.id,
            comment=comment.comment_text
        ).model_dump()
        for comment in comments
    ]
    return resp, HTTPStatus.OK


@post.route("/views", methods=["GET"])
def get_post_views():
    """Get a posts comments."""
    try:
        post_data = GetPost(post_id=request.args.get('post_id'))
    except ValidationError:
        return {'error': 'Invalid input: you probably did not include the post id.'}, HTTPStatus.BAD_REQUEST
    try:
        post: Post = get_post(session=get_db, post_data=post_data)
        if not post:
            return {'Error': f'post with id {post_data.post_id} does not exists'}, HTTPStatus.NOT_FOUND
        views: list[View] = list_post_views(session=get_db, post_data=post_data)
    except (OperationalError, IntegrityError) as e:
        print(e)
        # Send email to
        return {'Error': 'The application is experiencing a tempoary error. Please try again in a few minutes.'}, HTTPStatus.INTERNAL_SERVER_ERROR
    resp = [
        RepeatableActivityCreated(
            user_id=view.author_id,
            post_id=view.post_id,
            date_created=view.view_date,
            id=view.id
        ).model_dump()
        for view in views
    ]
    return resp, HTTPStatus.OK
