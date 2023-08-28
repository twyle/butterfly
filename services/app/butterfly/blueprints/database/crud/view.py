from ..schemas.activity import CreateActivity, GetRepeatableActivity
from sqlalchemy.orm import Session
from ..models.view import View
from ..models.user import User
from ..models.post import Post
from ..schemas.user import GetUser
from ..schemas.post import GetPost
from uuid import uuid4


def create_view(session: Session, activity: CreateActivity) -> View:
    with session() as db:
        view: View = View(
            author_id=activity.user_id,
            post_id=activity.post_id,
            id='View_' + str(uuid4())
        )
        db.add(view)
        db.commit()
        db.refresh(view)
    return view


def has_viewed(session: Session, activity: CreateActivity) -> View:
    with session() as db:
        view: View = db.query(View).filter(View.author_id==activity.user_id, View.post_id==activity.post_id).first()
        if view:
            return True
    return False

def list_user_views(session: Session, user_data: GetUser) -> list[View]:
    with session() as db:
        user: User = db.query(User).filter(User.id == user_data.user_id).first()
        views: list[View] = user.views
    return views

def list_post_views(session: Session, post_data: GetPost):
    with session() as db:
        post: Post = db.query(Post).filter(Post.id == post_data.post_id).first()
        views: list[View] = post.views
    return views
    