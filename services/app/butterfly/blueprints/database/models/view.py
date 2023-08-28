from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database import Base
from sqlalchemy import ForeignKey


class View(Base):
    __tablename__ = 'views'
    
    id: Mapped[str] = mapped_column(primary_key=True)
    author_id: Mapped[str] = mapped_column(ForeignKey('users.id'))
    post_id: Mapped[str] = mapped_column(ForeignKey('posts.id'))
    view_date: Mapped[datetime] = mapped_column(default_factory=datetime.utcnow)
    
    author = relationship('User', back_populates='views')
    post = relationship('Post', back_populates='views')