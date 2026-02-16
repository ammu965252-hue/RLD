from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    # keep existing fields for backward compatibility
    full_name = Column(String, nullable=True)
    name = Column(String, nullable=True)
    nickname = Column(String, nullable=True)
    password = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    role = Column(String, default="user", nullable=False, index=True)
    # Relationship to detections
    detections = relationship("Detection", back_populates="user", cascade="all, delete-orphan")

class Detection(Base):
    __tablename__ = "detections"

    id = Column(Integer, primary_key=True, index=True)
    disease = Column(String)
    confidence = Column(Float)
    severity = Column(String)
    image_path = Column(String)
    result_path = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    user = relationship("User", back_populates="detections")
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