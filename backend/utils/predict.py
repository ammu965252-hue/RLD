import os
import cv2
import json
from datetime import datetime
from ultralytics import YOLO

# =====================================================
# BASE PATHS
# =====================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "best.pt")

UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
RESULT_DIR = os.path.join(UPLOAD_DIR, "results")
HISTORY_FILE = os.path.join(BASE_DIR, "history.json")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)

# =====================================================
# LOAD MODEL
# =====================================================
model = YOLO(MODEL_PATH)

# =====================================================
# DISEASE INFO
# =====================================================
DISEASE_INFO = {
    "Blight": {
        "symptoms": [
            "Yellow-orange stripes on leaf blades",
            "Leaves wilt and roll up",
            "Creamy bacterial ooze",
            "V-shaped lesions from leaf tips"
        ],
        "treatment": [
            "Apply copper-based bactericides",
            "Remove infected leaves",
            "Avoid excessive nitrogen fertilizer"
        ],
        "prevention": [
            "Use certified disease-free seeds",
            "Ensure proper drainage",
            "Practice crop rotation"
        ]
    },

    "Brown Spot": {
        "symptoms": [
            "Brown circular spots",
            "Yellow halo around lesions",
            "Reduced grain quality"
        ],
        "treatment": [
            "Apply Mancozeb or Carbendazim",
            "Improve soil nutrition"
        ],
        "prevention": [
            "Balanced fertilization",
            "Seed treatment before planting"
        ]
    },

    "False Smut": {
        "symptoms": ["Green to yellow smut balls on panicles"],
        "treatment": ["Apply Propiconazole fungicide"],
        "prevention": ["Avoid excess nitrogen"]
    },

    "Healthy": {
        "symptoms": [],
        "treatment": [],
        "prevention": ["Maintain proper irrigation"]
    },

    "Leaf Smut": {
        "symptoms": ["Black streaks on leaves"],
        "treatment": ["Apply fungicide"],
        "prevention": ["Use disease-free seeds"]
    },

    "Rice Blast": {
        "symptoms": ["Diamond-shaped lesions"],
        "treatment": ["Spray Tricyclazole"],
        "prevention": ["Use blast-resistant varieties"]
    },

    "Stem Rot": {
        "symptoms": ["Rotting of stem base"],
        "treatment": ["Improve drainage"],
        "prevention": ["Avoid waterlogging"]
    },

    "Tungro": {
        "symptoms": ["Yellow-orange discoloration"],
        "treatment": ["Remove infected plants"],
        "prevention": ["Control leafhopper vectors"]
    }
}

# =====================================================
# SAVE HISTORY
# =====================================================
def save_history(entry):
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)

    history.insert(0, entry)

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

# =====================================================
# PREDICTION FUNCTION
# =====================================================
def predict_disease(image_path: str):
    filename = os.path.basename(image_path)

    results = model(
        image_path,
        imgsz=640,
        conf=0.5,
        iou=0.5,
        device="cpu"
    )[0]

    # ================= NO DETECTION =================
    if results.boxes is None or len(results.boxes) == 0:
        response = {
            "disease": "Healthy",
            "confidence": 99.0,
            "severity": "None",
            "description": "No disease detected.",
            "symptoms": [],
            "treatment": [],
            "prevention": DISEASE_INFO["Healthy"]["prevention"],
            "original_image": f"/uploads/{filename}",
            "result_image": f"/uploads/{filename}",
            "timestamp": datetime.now().isoformat()
        }
        save_history(response)
        return response

    # ================= BEST BOX =================
    best_idx = int(results.boxes.conf.argmax())
    cls_id = int(results.boxes.cls[best_idx])
    confidence = float(results.boxes.conf[best_idx]) * 100
    disease = results.names[cls_id].strip().title()

    plotted_img = results.plot()
    result_filename = f"result_{filename}"
    result_path = os.path.join(RESULT_DIR, result_filename)
    cv2.imwrite(result_path, plotted_img)

    info = DISEASE_INFO.get(disease, {})

    severity = (
        "Severe" if confidence >= 95 else
        "Moderate" if confidence >= 85 else
        "Mild"
    )

    response = {
        "disease": disease,
        "confidence": round(confidence, 2),
        "severity": severity,
        "description": f"{disease} detected on rice leaf.",
        "symptoms": info.get("symptoms", []),
        "treatment": info.get("treatment", []),
        "prevention": info.get("prevention", []),
        "original_image": f"/uploads/{filename}",
        "result_image": f"/uploads/results/{result_filename}",
        "timestamp": datetime.now().isoformat()
    }

    save_history(response)
    return response
