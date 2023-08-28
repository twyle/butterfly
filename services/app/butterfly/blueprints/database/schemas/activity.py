from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CreateActivity(BaseModel):
    user_id: str
    post_id: str
    

class ActivityCreated(CreateActivity):
    date_created: datetime
    
class RepeatableActivityCreated(ActivityCreated):
    id: str
    
class GetRepeatableActivity(BaseModel):
    id: str
    
class CreateComment(CreateActivity):
    comment: str
    
class CommentCreated(CreateComment):
    comment_id: str
    date_created: datetime