from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from ..database import Base


class Post(Base):
    __tablename__ = 'posts'
    
    id: Mapped[str] = mapped_column(primary_key=True)
    author_id: Mapped[str] = mapped_column(ForeignKey('users.id'))
    location: Mapped[str]
    text: Mapped[str]
    image_url: Mapped[str]
    date_published: Mapped[datetime] = mapped_column(default_factory=datetime.utcnow)
    date_updated: Mapped[datetime] = mapped_column(onupdate=datetime.utcnow, default_factory=datetime.utcnow)