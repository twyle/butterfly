from ..schemas.activity import CreateActivity
from sqlalchemy.orm import Session
from ..models.like import Like
from ..models.user import User
from ..models.post import Post
from ..schemas.user import GetUser
from ..schemas.post import GetPost


def create_like(session: Session, activity: CreateActivity) -> Like:
    with session() as db:
        like: Like = Like(
            author_id=activity.user_id,
            post_id=activity.post_id
        )
        db.add(like)
        db.commit()
        db.refresh(like)
    return like

def delete_like(session: Session, activity: CreateActivity) -> Like:
    with session() as db:
        like: Like = db.query(Like).filter(Like.author_id==activity.user_id, Like.post_id==activity.post_id).first()
        db.delete(like)
        db.commit()
    return like

def has_liked(session: Session, activity: CreateActivity) -> Like:
    with session() as db:
        like: Like = db.query(Like).filter(Like.author_id==activity.user_id, Like.post_id==activity.post_id).first()
        if like:
            return True
    return False

def list_user_likes(session: Session, user_data: GetUser) -> list[Like]:
    with session() as db:
        user: User = db.query(User).filter(User.id == user_data.user_id).first()
        likes: list[Like] = user.likes
    return likes

def list_post_likes(session: Session, post_data: GetPost):
    with session() as db:
        post: Post = db.query(Post).filter(Post.id == post_data.post_id).first()
        likes: list[Like] = post.likes
        for like in likes:
            like.author
    return likes

def get_key_like(session: Session, post_data: GetPost):
    from random import choice
    with session() as db:
        post: Post = db.query(Post).filter(Post.id == post_data.post_id).first()
        likes: list[Like] = post.likes
        for like in likes:
            like.author
    return choice(likes).author if likes else None
    