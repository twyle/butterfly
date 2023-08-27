from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database import Base
from sqlalchemy import ForeignKey


class Bookmark(Base):
    __tablename__ = 'bookmarks'
    
    author_id: Mapped[str] = mapped_column(ForeignKey('users.id'), primary_key=True)
    post_id: Mapped[str] = mapped_column(ForeignKey('posts.id'), primary_key=True)
    bookmark_date: Mapped[datetime] = mapped_column(default_factory=datetime.utcnow)
    
    author = relationship('Author', back_populates='bookmarks')
    post = relationship('Post', back_populates='bookmarks')