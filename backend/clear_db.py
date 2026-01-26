from database import SessionLocal
from models import Detection

def clear_sample_data():
    db = SessionLocal()
    try:
        # Delete all sample detections
        deleted_count = db.query(Detection).delete()
        db.commit()
        print(f"✅ Cleared {deleted_count} sample detections from database")
        print("Now you can upload real rice leaf images to populate the history with your actual detections!")
    except Exception as e:
        db.rollback()
        print(f"❌ Error clearing database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    clear_sample_data()