from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database import Base
from sqlalchemy import ForeignKey


class View(Base):
    __tablename__ = 'views'
    
    author_id: Mapped[str] = mapped_column(ForeignKey('users.id'), primary_key=True)
    post_id: Mapped[str] = mapped_column(ForeignKey('posts.id'), primary_key=True)
    view_date: Mapped[datetime] = mapped_column(default_factory=datetime.utcnow)
    
    author = relationship('Author', back_populates='views')
    post = relationship('Post', back_populates='views')