from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import shutil, os
from utils.predict import predict_disease

app = FastAPI(title="RiceGuard AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
RESULT_DIR = "uploads/results"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.post("/detect")
async def detect_disease(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        return {"error": "Invalid file"}

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = predict_disease(file_path)
    return result
