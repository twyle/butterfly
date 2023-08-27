from datetime import datetime, timedelta
from sqlalchemy.orm import Mapped, mapped_column
from ..database import Base
from flask import current_app
from ....extensions.extensions import bcrypt
from enum import Enum, auto
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError


class Role(Enum):
    User = auto()
    Admin = auto()


class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[str] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    email_address: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    registration_date: Mapped[datetime] = mapped_column(default_factory=datetime.utcnow)
    role: Mapped[str] = mapped_column(default='user')
    activated: Mapped[bool] = mapped_column(default=False)
    
    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password, password)
    
    @staticmethod
    def encode_auth_token(user_id: int):
        try:
            payload = {
                "exp": datetime.utcnow() + timedelta(days=0, hours=2),
                "iat": datetime.utcnow(),
                "sub": user_id,
            }
            return jwt.encode(payload, current_app.config.get("SECRET_KEY"), algorithm="HS256")
        except Exception as e:
            return e
        
    @staticmethod
    def decode_auth_token(auth_token: str):
        try:
            payload = jwt.decode(auth_token, current_app.config.get("SECRET_KEY"), algorithms="HS256")
            return payload["sub"]
        except (ExpiredSignatureError, InvalidTokenError) as e:
            raise e