from ..database.crud.user import get_random_user
from ..database.crud.post import get_posts
from ..database.crud.like import list_post_likes, get_key_like, has_liked
from ..database.crud.comment import get_key_comment, list_post_comments
from ..database.crud.bookmark import has_bookmarked
from ..database.database import get_db
from ..database.models import (
    User, Post, Like, Bookmark, Comment
)
from ..database.schemas.post import (
    GetPosts, PostAuthor, GetPost, PostLike, KeyComment, PostSchema
)
from ..database.schemas.activity import CreateActivity
from flask import url_for
from pydantic import ValidationError
from sqlalchemy.exc import OperationalError, IntegrityError
from datetime import datetime

def load_posts(offset: int = 0, limit: int = 10) -> None:
    user: User = get_random_user(get_db)
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
            profile_picture=url_for('static', filename=f'img/{post.author.profile_picture_url}'),
            name=post.author.first_name
        )
        post_likes = [
            PostAuthor(
                id=like.author.id,
                profile_picture=url_for('static', filename=f'img/{like.author.profile_picture_url}'),
                name=like.author.first_name
            )
            for like in list_post_likes(session=get_db, post_data=GetPost(post_id=post.id))
        ]
        key_like: User = get_key_like(session=get_db, post_data=GetPost(post_id=post.id))
        if key_like:
            key_like = PostAuthor(
                id=key_like.id,
                profile_picture=url_for('static', filename=f'img/{key_like.profile_picture_url}'),
                name=key_like.first_name
            )
        post_like: PostLike = PostLike(
            liked=has_liked(get_db, CreateActivity(user_id=user.id, post_id=post.id)),
            liked_by=post_likes,
            key_like=key_like,
            likes_count=len(post_likes)
        )
        key_comment: Comment = get_key_comment(session=get_db, post_data=GetPost(post_id=post.id))
        if key_comment:
            key_comment_author = PostAuthor(
                id=key_comment.author.id,
                profile_picture=url_for('static', filename=f'img/{key_comment.author.profile_picture_url}'),
                name=key_comment.author.first_name,
            )
            key_comment: KeyComment = KeyComment(
                author=key_comment_author,
                text=key_comment.comment_text,
                comments_count=len(list_post_comments(session=get_db, post_data=GetPost(post_id=post.id)))
            )
        post_schema: PostSchema = PostSchema(
            id=post.id,
            text=post.text,
            image=url_for('static', filename=f'img/{post.image_url}'),
            location=post.location,
            date_published=str(int((post.date_published - datetime.now()).seconds/60)),
            author=post_author,
            like=post_like,
            key_comment=key_comment,
            bookmarked=has_bookmarked(get_db, CreateActivity(user_id=user.id, post_id=post.id))
        ).model_dump()
        created_posts.append(post_schema)
    return created_posts