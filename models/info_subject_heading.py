from sqlalchemy import Column, Integer

from .base import Base

class InfoSubjectHeading(Base):
    __tablename__ = "info_subject_headings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    info_id = Column(Integer)
    subject_heading_id = Column(Integer)
    
