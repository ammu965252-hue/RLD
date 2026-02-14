from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Detection(Base):
    __tablename__ = "detections"

    id = Column(Integer, primary_key=True, index=True)
    disease = Column(String)
    confidence = Column(Float)
    severity = Column(String)
    image_path = Column(String)
    result_path = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True)
    detection_id = Column(String, index=True)
    rating = Column(Integer)
    comments = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class ForumPost(Base):
    __tablename__ = "forum_posts"
    id = Column(Integer, primary_key=True)
    user = Column(String)
    title = Column(String)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)