from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PostBase(BaseModel):
    location: str
    text: str
    author_id: str


class CreatePost(PostBase):
    pass

class UpdatePost(BaseModel):
    post_id: str
    author_id: str
    location: Optional[str]
    text: Optional[str]

class CreatedPost(PostBase):
    date_published: datetime
    id: str
    image_url: str
    likes: list
    
class GetPost(BaseModel):
    post_id: str
    
class GetPosts(BaseModel):
    offset: Optional[int] = 0
    limit: Optional[int] = 10
    
class PostAuthor(BaseModel):
    id: str
    profile_picture: str
    name: str
    
class PostLike(BaseModel):
    liked: bool
    liked_by: Optional[list[PostAuthor]] = Field(default_factory=list)
    key_like: Optional[PostAuthor] = None
    likes_count: Optional[int] = Field(default=0)
    
class PostSchema(BaseModel):
    id: str
    text: str
    image: str
    author: PostAuthor
    date_published: str
    location: str
    like: PostLike
    bookmarked: bool