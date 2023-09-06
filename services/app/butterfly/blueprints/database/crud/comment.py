from ..schemas.activity import CreateComment, CreateActivity
from sqlalchemy.orm import Session
from ..models.comment import Comment
from ..models.user import User
from ..models.post import Post
from ..schemas.user import GetUser
from ..schemas.post import GetPost
from uuid import uuid4


def create_comment(session: Session, comment_data: CreateComment) -> Comment:
    with session() as db:
        comment: Comment = Comment(
            author_id=comment_data.user_id,
            post_id=comment_data.post_id,
            id='Comment_' + str(uuid4()),
            comment_text=comment_data.comment
        )
        db.add(comment)
        db.commit()
        db.refresh(comment)
    return comment


def has_commented(session: Session, activity: CreateActivity) -> Comment:
    with session() as db:
        comment: Comment = db.query(Comment).filter(Comment.author_id==activity.user_id, Comment.post_id==activity.post_id).first()
        if comment:
            return True
    return False

def list_user_comments(session: Session, user_data: GetUser) -> list[Comment]:
    with session() as db:
        user: User = db.query(User).filter(User.id == user_data.user_id).first()
        comments: list[Comment] = user.comments
    return comments

def list_user_post_comments(session: Session, activity: CreateActivity) -> list[Comment]:
    with session() as db:
        comments: list[Comment] = db.query(Comment).filter(Comment.author_id == activity.user_id, Comment.post_id==activity.post_id).all()
    return comments

def list_post_comments(session: Session, post_data: GetPost, offset: int = 0, limit: int = 5):
    with session() as db:
        post: Post = db.query(Post).filter(Post.id == post_data.post_id).first()
        comments: list[Comment] = post.comments
        for comment in comments:
            comment.author
        print(offset,limit)
    return comments[offset:limit]
    
def get_key_comment(session: Session, post_data: GetPost):
    from random import choice
    with session() as db:
        post: Post = db.query(Post).filter(Post.id == post_data.post_id).first()
        comments: list[Comment] = post.comments
        for comment in comments:
            comment.author
    return choice(comments) if comments else None