from pydantic import BaseModel
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
    
class GetPost(BaseModel):
    post_id: str
    
class GetPosts(BaseModel):
    offset: Optional[int] = 0
    limit: Optional[int] = 10