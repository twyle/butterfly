from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database import Base
from sqlalchemy import ForeignKey


class Like(Base):
    __tablename__ = 'likes'
    
    author_id: Mapped[str] = mapped_column(ForeignKey('users.id'), primary_key=True)
    post_id: Mapped[str] = mapped_column(ForeignKey('posts.id'), primary_key=True)
    like_date: Mapped[datetime] = mapped_column(default_factory=datetime.utcnow)
    
    author = relationship('User', back_populates='likes')
    post = relationship('Post', back_populates='likes')