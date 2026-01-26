from fastapi import FastAPI, File, UploadFile, WebSocket, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import shutil
import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

from utils.pdf_report import generate_pdf
from database import SessionLocal
from models import Feedback, ForumPost, Detection
from utils.predict import DISEASE_INFO

# Load environment variables from .env file
load_dotenv()

# Validate critical environment variables at startup
admin_token = os.getenv("ADMIN_TOKEN")
if not admin_token:
    raise RuntimeError("ADMIN_TOKEN environment variable is required for admin access")

# =====================================================
# APP INIT
# =====================================================
app = FastAPI(title="RiceGuard AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8001", "http://localhost:8001"],  # Restricted to specific frontend origins
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# PATHS
# =====================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
RESULT_DIR = os.path.join(UPLOAD_DIR, "results")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)

# =====================================================
# STATIC FILES (FOR IMAGES)
# =====================================================
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# =====================================================
# DETECT API
# =====================================================
@app.post("/detect")
async def detect_disease(file: UploadFile = File(...)):
    print("📥 Detection request received")

    # Secure file upload validation
    allowed_types = ["image/jpeg", "image/png", "image/webp"]
    if file.content_type not in allowed_types:
        print("❌ Invalid file type")
        return {"error": "Only JPEG, PNG, and WebP images are allowed"}

    # Check file size (5MB limit)
    max_size = 5 * 1024 * 1024  # 5MB
    file.file.seek(0, 2)  # Seek to end
    size = file.file.tell()
    file.file.seek(0)  # Reset to beginning
    if size > max_size:
        print("❌ File too large")
        return {"error": "File size exceeds 5MB limit"}

    print(f"📁 Processing file: {file.filename}")

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        print("✅ File saved successfully")
    except Exception as e:
        print(f"❌ File save error: {e}")
        return {"error": "Failed to save file"}

    # 🔥 MODEL PREDICTION
    try:
        from utils.predict import predict_disease
        result = predict_disease(file_path)
        print(f"✅ Prediction successful: {result['disease']}")
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return {"error": "Prediction failed"}

    # 💾 SAVE DETECTION TO DATABASE
    db = SessionLocal()
    try:
        detection = Detection(
            disease=result["disease"],
            confidence=result["confidence"],
            severity=result["severity"],
            image_path=result["original_image"],
            result_path=result["result_image"]
        )
        db.add(detection)
        db.commit()
        db.refresh(detection)  # Get the auto-generated ID

        # Add detection ID to response
        result["detection_id"] = detection.id
        print(f"✅ Detection saved to database: ID {detection.id}, Disease: {detection.disease}")
        return result

    except Exception as e:
        db.rollback()
        print(f"❌ Database error: {e}")
        print(f"   Failed to save detection: {result['disease']} - {result['confidence']}%")
        return result  # Return result even if DB save fails
    finally:
        db.close()

    print("📤 Returning result")
    return result


# =====================================================
# HISTORY API (UPDATED TO READ FROM DATABASE)
# =====================================================
@app.get("/history")
def get_history():
    db = SessionLocal()
    try:
        # Query all detections from database, ordered by newest first
        detections = db.query(Detection).order_by(Detection.created_at.desc()).all()
        
        # Format response to match frontend expectations
        history = [
            {
                "id": d.id,
                "disease": d.disease,
                "confidence": d.confidence,
                "severity": d.severity,
                "original_image": d.image_path,
                "result_image": d.result_path,
                "timestamp": d.created_at.isoformat()  # Convert datetime to ISO string
            }
            for d in detections
        ]
        return history
    finally:
        db.close()


# =====================================================
# DELETE DETECTION API
# =====================================================
@app.delete("/delete/{detection_id}")
def delete_detection(detection_id: int):
    db = SessionLocal()
    try:
        detection = db.query(Detection).filter(Detection.id == detection_id).first()
        if not detection:
            raise HTTPException(status_code=404, detail="Detection not found")
        
        # Delete the detection
        db.delete(detection)
        db.commit()
        
        # Optionally delete the image files
        try:
            if os.path.exists(os.path.join(BASE_DIR, detection.image_path.lstrip('/'))):
                os.remove(os.path.join(BASE_DIR, detection.image_path.lstrip('/')))
            if os.path.exists(os.path.join(BASE_DIR, detection.result_path.lstrip('/'))):
                os.remove(os.path.join(BASE_DIR, detection.result_path.lstrip('/')))
        except Exception as e:
            print(f"Warning: Could not delete image files: {e}")
        
        return {"message": "Detection deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting detection: {str(e)}")
    finally:
        db.close()


# =====================================================
# ADMIN OVERVIEW (DATABASE INSPECTION)
# =====================================================
@app.get("/admin/overview")
def admin_overview(request: Request):
    # Secure admin access with token validation
    token = request.headers.get("X-Admin-Token")
    if not token or token != admin_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    db = SessionLocal()
    try:
        # Query all detections ordered by newest first
        detections = db.query(Detection).order_by(Detection.created_at.desc()).all()
        
        result = []
        for d in detections:
            # Query related feedback for this detection
            feedback_list = db.query(Feedback).filter(Feedback.detection_id == str(d.id)).all()
            feedback_data = [
                {
                    "rating": f.rating,
                    "comments": f.comments,
                    "created_at": f.created_at.strftime("%Y-%m-%d %H:%M:%S")
                }
                for f in feedback_list
            ]
            
            result.append({
                "id": d.id,
                "disease": d.disease,
                "confidence": d.confidence,
                "severity": d.severity,
                "created_at": d.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "image_path": d.image_path,
                "result_path": d.result_path,
                "feedback": feedback_data
            })
        
        return result
    finally:
        db.close()


# =====================================================
# GENERATE REPORT
# =====================================================
@app.post("/generate_report")
def generate_report(data: dict):
    import uuid
    file_name = f"report_{uuid.uuid4()}.pdf"
    file_path = os.path.join(RESULT_DIR, file_name)
    generate_pdf(data, file_path)
    return {"file_url": f"/uploads/results/{file_name}"}


# =====================================================
# FEEDBACK SYSTEM
# =====================================================
@app.post("/feedback")
def submit_feedback(data: dict):
    db = SessionLocal()
    feedback = Feedback(
        detection_id=data["detection_id"],
        rating=data["rating"],
        comments=data.get("comments", "")
    )
    db.add(feedback)
    db.commit()
    db.close()
    return {"message": "Feedback submitted"}


# =====================================================
# FORUM
# =====================================================
@app.get("/forum")
def get_forum_posts():
    db = SessionLocal()
    posts = db.query(ForumPost).all()
    db.close()
    return [{"id": p.id, "user": p.user, "title": p.title, "content": p.content, "created_at": p.created_at} for p in posts]

@app.post("/forum")
def add_forum_post(data: dict):
    db = SessionLocal()
    post = ForumPost(
        user=data["user"],
        title=data["title"],
        content=data["content"]
    )
    db.add(post)
    db.commit()
    db.close()
    return {"message": "Post added"}


# =====================================================
# RULE-BASED CHATBOT (OFFLINE, DISEASE_INFO ONLY)
# =====================================================
@app.post("/chatbot")
def chatbot_response(data: dict):
    user_message = data["message"].lower().strip()
    
    # Available diseases from DISEASE_INFO
    diseases = list(DISEASE_INFO.keys())
    
    # Detect disease mentioned in message
    detected_disease = None
    for disease in diseases:
        if disease.lower() in user_message:
            detected_disease = disease
            break
    
    if not detected_disease:
        return {"response": "I can help only with rice leaf diseases. Please specify the disease name."}
    
    # Define intent keywords
    intents = {
        "symptoms": ["symptom", "sign", "look like", "appear", "show"],
        "treatment": ["treat", "cure", "medicine", "fix", "heal"],
        "prevention": ["prevent", "avoid", "stop", "protect", "safe"],
        "severity": ["severity", "level", "bad", "serious", "worse"]
    }
    
    # Detect intent
    detected_intent = None
    for intent, keywords in intents.items():
        if any(keyword in user_message for keyword in keywords):
            detected_intent = intent
            break
    
    if not detected_intent:
        return {"response": "Please ask about symptoms, treatment, prevention, or severity of the disease."}
    
    # Get disease info (use High severity if available, else first available)
    disease_data = DISEASE_INFO[detected_disease]
    severity = "High" if "High" in disease_data else list(disease_data.keys())[0]
    info = disease_data[severity]
    
    # Build response from DISEASE_INFO
    if detected_intent in info and info[detected_intent]:
        response = f"For {detected_disease} ({severity} severity): {', '.join(info[detected_intent])}"
    else:
        response = "Information is not available. Please consult an agricultural expert."
    
    return {"response": response}


# =====================================================
# EXPERT CONSULTATION (CONTACT FORM)
# =====================================================
@app.post("/contact")
def contact_expert(data: dict):
    try:
        msg = MIMEText(f"Message: {data['message']}\nFrom: {data['email']}")
        msg['Subject'] = "Expert Consultation Request - RiceGuard"
        msg['From'] = "noreply@riceguard.com"  # Replace with your email
        msg['To'] = "expert@example.com"  # Replace with expert email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("your-email@gmail.com", "your-password")  # Use app password
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        return {"message": "Message sent to expert"}
    except:
        return {"error": "Failed to send message"}


# =====================================================
# WEBSOCKET CHAT FOR EXPERT CONSULTATION
# =====================================================
@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Connected to expert chat. How can I help?")
    while True:
        try:
            data = await websocket.receive_text()
            # Simulate expert response (integrate with real logic)
            response = f"Expert: {data} - Please provide more details or contact via email."
            await websocket.send_text(response)
        except:
            break
