from ..blueprints.database.schemas.user import UserCreate
from ..blueprints.database.schemas.post import CreatePost
from ..blueprints.database.models import User, Post, Like, Comment, Bookmark
from ..blueprints.database.database import get_db
from ..blueprints.database.crud.user import create_user
from ..blueprints.database.crud.post import create_post
from faker import Faker
from datetime import datetime, timedelta
import random
from uuid import uuid4


fake = Faker()

def generate_users(count: int = 10) -> list[UserCreate]:
    """Generate ten random users."""
    first_names = (fake.name() for _ in range(count))
    last_names = (fake.name() for _ in range(count))
    emails = (fake.email() for i in range(count))
    profile_pictures = [f'profile-{i}.jpg' for i in range(count)]
    return [
        User(
            id='User_' + str(uuid4()),
            first_name=first_name,
            last_name=last_name,
            email_address=email,
            password=User.hash_password('password'),
            profile_picture_url=image
        ) 
        for first_name, last_name, email, image in zip(first_names, last_names, emails, profile_pictures)
    ]
    
def generate_posts(authors: list[User], count: int = 100) -> list[Post]:
    """Generate posts."""
    cities = [fake.city() for _ in range(10)]
    posts_text = [fake.text() for _ in range(count)]
    dates_published = (datetime.now() + timedelta(minutes=random.randint(1,60)) for _ in range(count))
    post_images = [f'feed-{i}.jpg' for i in range(1,8)]
    return [
        Post(
            id='Post_' + str(uuid4()),
            author_id=random.choice(authors).id,
            location=random.choice(cities),
            text=text,
            image_url=random.choice(post_images),
            date_published=d
        )
        for text, d in zip(posts_text, dates_published)
    ]
    
def generate_likes(users: list[User], posts: list[Post], likes_count: int = 100) -> list[Like]:
    """Generate likes."""
    likes: list[Like] = []
    ids = set()
    for _ in range(likes_count):
        author_id: str = random.choice(users).id
        post_id: str = random.choice(posts).id
        like: Like = Like(author_id=author_id, post_id=post_id)
        if (author_id, post_id) not in ids:
            likes.append(like)
        ids.add((author_id, post_id))
    return likes

def generate_bookmarks(users: list[User], posts: list[Post], bookmarks_count: int = 100) -> list[Bookmark]:
    """Generate bookmarks."""
    bookmarks: list[Bookmark] = []
    ids = set()
    for _ in range(bookmarks_count):
        author_id: str = random.choice(users).id
        post_id: str = random.choice(posts).id
        bookmark: bookmark = Bookmark(author_id=author_id, post_id=post_id)
        if (author_id, post_id) not in ids:
            bookmarks.append(bookmark)
        ids.add((author_id, post_id))
    return bookmarks

def generate_comments(users: list[User], posts: list[Post], comments_count: int = 500) -> list[Like]:
    """Generate likes."""
    comments: list[Comment] = []
    ids = set()
    for _ in range(comments_count):
        author_id: str = random.choice(users).id
        post_id: str = random.choice(posts).id
        comment: comment = Comment(
            id='Comment_' + str(uuid4()),
            author_id=author_id, 
            post_id=post_id, 
            comment_text=fake.text() )
        if (author_id, post_id) not in ids:
            comments.append(comment)
        ids.add((author_id, post_id))
    return comments

def add_user(user: User) -> User:
    with get_db() as session:
        session.add(user)
        session.commit()
        session.refresh(user)
    return user

def add_post(post: Post) -> Post:
    with get_db() as session:
        session.add(post)
        session.commit()
        session.refresh(post)
    return post

def add_likes(likes: list[Like]) -> None:
    with get_db() as session:
        for like in likes:
            session.add(like)
        session.commit()
        
def add_bookmarks(bookmarks: list[Bookmark]) -> None:
    with get_db() as session:
        for bookmark in bookmarks:
            session.add(bookmark)
        session.commit()
    
def add_comments(comments: list[Comment]) -> None:
    with get_db() as session:
        for comment in comments:
            session.add(comment)
        session.commit()
    
def generate_data(
    user_count: int = 20, 
    posts_count: int = 200, 
    likes_count: int = 500, 
    comments_count: int = 200,
    bookmarks_count: int = 600
    ):
    users = generate_users(user_count)
    users = [
        add_user(user) for user in users
    ]
    posts: list[Post] = generate_posts(users, count=posts_count)
    posts: list[Post] = [
        add_post(post) for post in posts
    ]
    likes: list[Like] = generate_likes(users, posts, likes_count=likes_count)
    add_likes(likes)
    
    comments: list[Comment] = generate_comments(users, posts, comments_count=comments_count)
    add_comments(comments)
    
    bookmarks: list[Bookmark] = generate_bookmarks(users, posts, bookmarks_count=bookmarks_count)
    add_bookmarks(bookmarks)
    