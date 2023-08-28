from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database import Base
from sqlalchemy import ForeignKey


class Comment(Base):
    __tablename__ = 'comments'
    
    id: Mapped[str] = mapped_column(primary_key=True)
    author_id: Mapped[str] = mapped_column(ForeignKey('users.id'))
    post_id: Mapped[str] = mapped_column(ForeignKey('posts.id'))
    comment_text: Mapped[str]
    comment_date: Mapped[datetime] = mapped_column(default_factory=datetime.utcnow)
    
    author = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')