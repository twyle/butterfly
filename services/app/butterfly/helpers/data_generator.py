from ..blueprints.database.schemas.user import UserCreate
from ..blueprints.database.schemas.post import CreatePost
from ..blueprints.database.models import User, Post
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
    post_images = [f'feed-{i}.jpg' for i in range(8)]
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
    
    
def generate_data(user_count: int = 10, posts_count: int = 100):
    users = generate_users(user_count)
    users = [
        add_user(user) for user in users
    ]
    posts: list[Post] = generate_posts(users)
    posts: list[Post] = [
        add_post(post) for post in posts
    ]
    