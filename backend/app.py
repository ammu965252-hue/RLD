from fastapi import FastAPI, File, UploadFile, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import shutil
import os
import json
import openai
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

from utils.pdf_report import generate_pdf
from database import SessionLocal
from models import Feedback, ForumPost, Detection

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key from environment variable (secure approach)
openai.api_key = os.getenv("OPENAI_API_KEY")

# =====================================================
# APP INIT
# =====================================================
app = FastAPI(title="RiceGuard AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # frontend access
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# PATHS
# =====================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
RESULT_DIR = os.path.join(UPLOAD_DIR, "results")
HISTORY_FILE = os.path.join(BASE_DIR, "history.json")

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

    if not file.content_type.startswith("image/"):
        print("❌ Invalid file type")
        return {"error": "Invalid image file"}

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
# HISTORY API (REAL DATA)
# =====================================================
@app.get("/history")
def get_history():
    if not os.path.exists(HISTORY_FILE):
        return []

    with open(HISTORY_FILE, "r") as f:
        return json.load(f)


# =====================================================
# CLEAR HISTORY (OPTIONAL)
# =====================================================
@app.delete("/history")
def clear_history():
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
    return {"message": "History cleared"}


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
# ENHANCED CHATBOT WITH AI
# =====================================================
@app.post("/chatbot")
def chatbot_response(data: dict):
    user_message = data["message"]
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """
You are RiceGuard AI, a knowledgeable and helpful chatbot specialized ONLY in rice leaf diseases.

YOUR ROLE:
- Answer any user question related to rice leaf diseases.
- Help farmers and users understand symptoms, causes, prevention, and treatment of rice leaf diseases.
- Respond clearly, accurately, and in a friendly manner.

DOMAIN RESTRICTION:
You must answer ONLY questions related to:
- Rice leaf diseases
- Symptoms on rice leaves
- Causes of rice diseases
- Disease prevention methods
- Treatment and management practices
- Crop care related to rice leaf health

If the user asks anything outside rice leaf disease topics, politely reply:
"I can help only with questions related to rice leaf diseases."

ANSWERING GUIDELINES:
- Do not guess or invent information.
- If the question is unclear, ask a short follow-up question.
- If information is insufficient, say so honestly.
- Prefer simple explanations suitable for farmers.
- Mention the possible disease name when relevant.
- Suggest general treatment and prevention steps.
- Add a caution note for severe cases.

SAFETY RULES:
- Do not provide exact pesticide dosages unless clearly known.
- Do not promote excessive chemical usage.
- Prefer safe and sustainable farming practices.
- For serious or widespread disease, advise consulting an agricultural expert.

TONE & STYLE:
- Friendly, calm, and supportive
- Simple language
- No unnecessary technical jargon
- Short but informative responses

Your goal is to act as a trusted digital assistant for rice leaf disease guidance.
"""},
                {"role": "user", "content": user_message}
            ]
        )
        ai_response = response.choices[0].message.content
    except:
        ai_response = "Sorry, I'm unable to respond right now. Please try again later."
    return {"response": ai_response}


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
