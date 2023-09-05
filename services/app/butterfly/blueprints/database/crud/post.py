from sqlalchemy.orm import Session
from ..models.post import Post
from ..schemas.post import (
    CreatePost, GetPosts, GetPost, UpdatePost
)
from werkzeug.datastructures import FileStorage
from flask import current_app
from uuid import uuid4
from werkzeug.utils import secure_filename
import os
import secrets
from typing import Callable


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def get_file_extension(filename: str) -> str:
    if '.' in filename and filename.rsplit('.', 1)[1].lower():
        return filename.rsplit('.', 1)[1].lower()
    return ''

def allowed_file(filename: str) -> bool:
    file_extension: str = get_file_extension(filename)
    if file_extension and file_extension in ALLOWED_EXTENSIONS:
        return True
    return False


def save_post_photo_locally(post_image: dict) -> None:
    """Save the uploadeded post image."""
    file: FileStorage = post_image['post_image']
    upload_folder = os.path.join(current_app.root_path, 'static', 'img')
    if file and allowed_file(file.filename):
        filename = f'{secrets.token_hex(8)}.{get_file_extension(file.filename)}' 
        # Use celery task
        file.save(os.path.join(upload_folder, filename))
        return filename
    return ''


def save_post_photo_aws_s3(post_image: dict) -> None:
    """Save the uploadeded post image."""
    file: FileStorage = post_image['post_image']
    if file and allowed_file(file.filename):
        filename = f'{secrets.token_hex(8)}.{get_file_extension(file.filename)}'
        # Use celery task
        return filename
    return ''

def no_save_post_photo(post_image: dict) -> None:
    """Save the uploadeded post image."""
    file: FileStorage = post_image['post_image']
    if file and allowed_file(file.filename):
        filename = f'{secrets.token_hex(8)}.{get_file_extension(file.filename)}'
        return filename
    return ''


def save_post_photo(post_image: dict, save_location: str = '') -> str:
    """Save the uploadeded post image."""
    save_photo_funcs: dict[str, Callable[[dict], str]] = {
        'locally': save_post_photo_locally,
        'aws_s3': save_post_photo_aws_s3,
        'default': no_save_post_photo
    }
    if save_photo_funcs.get(save_location):
        filename: str = save_photo_funcs[save_location](post_image)
    else:
        filename: str = save_photo_funcs['default'](post_image)
    return filename


def create_post(post_data: CreatePost, post_image: dict, session: Session):
    post_image_url: str = save_post_photo(post_image)
    post: Post = Post(
        id='Post_' + str(uuid4()),
        author_id=post_data.author_id,
        location=post_data.location,
        text=post_data.text,
        image_url=post_image_url
    )
    with session() as db:
        db.add(post)
        db.commit()
        db.refresh(post)
    return post

def update_post(post_data: UpdatePost, post_image: dict, session: Session):
    post_image_url: str = save_post_photo(post_image)
    with session() as db:
        post: Post = db.query(Post).filter(Post.id == post_data.post_id).first()
        if post_data.location:
            post.location = post_data.location
        if post_data.text:
            post.text = post_data.text
        if post_image_url:
            post.image_url = post_image_url
        db.commit()
        db.refresh(post)
    return post

def get_post(session: Session, post_data: GetPost):
    with session() as db:
        post = db.query(Post).filter(Post.id == post_data.post_id).first()
    return post

def get_posts(session: Session, post_data: GetPosts):
    with session() as db:
        posts: list[Post] = db.query(Post).offset(post_data.offset).limit(post_data.limit).all()
        for post in posts:
            post.author
        return posts

def delete_post(session: Session, post_data: GetPost):
    with session() as db:
        post = db.query(Post).filter(Post.id == post_data.post_id).first()
        db.delete(post)
        db.commit()
        
    return post