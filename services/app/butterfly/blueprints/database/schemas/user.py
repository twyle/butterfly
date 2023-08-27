from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
  first_name: str
  last_name: str
  email_address: str

  
class UserCreate(UserBase):
    password: str
    role: str = 'user'
    activated: bool = False
    
class UserCreated(UserBase):
    id: str
    activation_token: str

class User(UserBase):
    id: str
    
    class Config:
        from_attributes = True
        
class GetUser(BaseModel):
    user_id: str
    
class GetUsers(BaseModel):
    offset: Optional[int] = 0
    limit: Optional[int] = 10
    
class ActivateUser(BaseModel):
    user_id: str
    activation_token: str
    
class LoginUser(BaseModel):
    email_address: str
    password: str
    
class LoggedInUser(BaseModel):
    email_address: str
    access_token: str
    refresh_token: str
    
class RequestPasswordReset(BaseModel):
    user_id: str
    email_address: str
    
class RequestPasswordResetToken(RequestPasswordReset):
    password_reset_token: str
    
class PasswordReset(BaseModel):
    email_address: str
    password_reset_token: str
    password: str
    confirm_password: str