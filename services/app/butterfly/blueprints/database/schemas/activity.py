from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CreateActivity(BaseModel):
    user_id: str
    post_id: str
    

class ActivityCreated(CreateActivity):
    date_created: datetime
    
    