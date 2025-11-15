from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime

from .base import Base

class Info(Base):
    __tablename__ = "infos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    article_id = Column(Integer)
    title = Column(String(255))
    excerpt = Column(Text)
    description = Column(Text)
    description_text = Column(Text)
    alias = Column(Text)
    source = Column(Text)
    publish_date = Column(DateTime)
    
