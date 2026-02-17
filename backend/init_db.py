"""
Initialize SQLite database with all tables.
This script creates tables only if they don't exist (idempotent).
Safe to run multiple times without losing data.
"""

from database import Base, engine, init_db
from models import User, Detection, Feedback, ForumPost, PromotionAudit

# This creates all tables that don't already exist
init_db()

print("✅ Database setup complete!")
print("📊 Tables created/verified:")
print("   - users (User model)")
print("   - detections (Detection model)")
print("   - feedback (Feedback model)")
print("   - forum_posts (ForumPost model)")
print("   - promotion_audit (PromotionAudit model)")
