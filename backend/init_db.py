"""
Initialize all SQLAlchemy models in the database.
This script creates all tables defined in models.py including:
- User
- Detection
- Feedback
- ForumPost

Existing tables will not be affected.
"""

from database import Base, engine
from models import User, Detection, Feedback, ForumPost

# Create all tables
Base.metadata.create_all(bind=engine)

print("✅ Database initialized successfully!")
print("📊 Created tables:")
print("   - users (User model)")
print("   - detections (Detection model)")
print("   - feedback (Feedback model)")
print("   - forum_posts (ForumPost model)")
