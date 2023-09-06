from pydantic import BaseModel
from .post import PostAuthor
    
class CommentSchema(BaseModel):
    author: PostAuthor
    text: str