from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import shutil
import os

from utils.predict import predict_disease

app = FastAPI(title="RiceGuard AI Backend")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Upload directory
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Serve uploaded + result images
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.post("/detect")
async def detect_disease(file: UploadFile = File(...)):

    # Validate file type
    if not file.content_type.startswith("image/"):
        return {"error": "Invalid file type. Please upload an image."}

    # Save uploaded image
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run prediction
    try:
        result = predict_disease(file_path)
    except Exception as e:
        return {"error": f"Prediction failed: {str(e)}"}

    # OPTIONAL: include original image path (clean & consistent)
    result["original_image"] = f"/uploads/{file.filename}"

    return result
