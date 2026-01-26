from datetime import datetime, timedelta
from database import SessionLocal
from models import Detection
import random

# Sample data
diseases = ["Rice Blast", "Brown Spot", "Leaf Smut", "False Smut", "Stem Rot", "Healthy"]
severities = ["Mild", "Moderate", "Severe", "None"]

def populate_sample_data():
    db = SessionLocal()
    try:
        # Clear existing data
        db.query(Detection).delete()
        db.commit()

        # Generate 20 past detections
        for i in range(20):
            # Random date in the past 30 days
            days_ago = random.randint(1, 30)
            hours_ago = random.randint(0, 23)
            minutes_ago = random.randint(0, 59)
            created_at = datetime.now() - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)

            disease = random.choice(diseases)
            severity = "None" if disease == "Healthy" else random.choice(severities[:3])
            confidence = round(random.uniform(85, 99), 2)

            detection = Detection(
                disease=disease,
                confidence=confidence,
                severity=severity,
                image_path=f"/uploads/sample_{i+1}.svg",
                result_path=f"/uploads/results/result_sample_{i+1}.svg",
                created_at=created_at
            )
            db.add(detection)

        db.commit()
        print("✅ Successfully populated database with 20 sample detections from the past 30 days")

    except Exception as e:
        db.rollback()
        print(f"❌ Error populating database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    populate_sample_data()