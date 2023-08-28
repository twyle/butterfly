from ..schemas.activity import CreateActivity
from sqlalchemy.orm import Session
from ..models.bookmark import Bookmark
from ..models.user import User
from ..models.post import Post
from ..schemas.user import GetUser
from ..schemas.post import GetPost


def create_bookmark(session: Session, activity: CreateActivity) -> Bookmark:
    with session() as db:
        bookmark: Bookmark = Bookmark(
            author_id=activity.user_id,
            post_id=activity.post_id
        )
        db.add(bookmark)
        db.commit()
        db.refresh(bookmark)
    return bookmark

def delete_bookmark(session: Session, activity: CreateActivity) -> Bookmark:
    with session() as db:
        bookmark: Bookmark = db.query(Bookmark).filter(Bookmark.author_id==activity.user_id, Bookmark.post_id==activity.post_id).first()
        db.delete(bookmark)
        db.commit()
    return bookmark

def has_bookmarked(session: Session, activity: CreateActivity) -> Bookmark:
    with session() as db:
        bookmark: Bookmark = db.query(Bookmark).filter(Bookmark.author_id==activity.user_id, Bookmark.post_id==activity.post_id).first()
        if bookmark:
            return True
    return False

def list_user_bookmarks(session: Session, user_data: GetUser) -> list[Bookmark]:
    with session() as db:
        user: User = db.query(User).filter(User.id == user_data.user_id).first()
        bookmarks: list[Bookmark] = user.bookmarks
    return bookmarks

def list_post_bookmarks(session: Session, post_data: GetPost):
    with session() as db:
        post = db.query(Post).filter(Post.id == post_data.post_id).first()
        bookmarks: list[Bookmark] = post.bookmarks
    return bookmarks
    