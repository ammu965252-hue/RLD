import os
import cv2
from ultralytics import YOLO

# =====================================================
# BASE PATHS (SAFE FOR LOCAL / SERVER / DEPLOYMENT)
# =====================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "best.pt")

UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
RESULT_DIR = os.path.join(UPLOAD_DIR, "results")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)

# =====================================================
# LOAD YOLOv8 MODEL (NEW TRAINED MODEL)
# =====================================================
model = YOLO(MODEL_PATH)

# =====================================================
# DISEASE INFORMATION (KEYS MUST MATCH MODEL CLASSES)
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
        "symptoms": [
            "Green to yellow smut balls on panicles",
            "Powdery spores inside balls"
        ],
        "treatment": [
            "Remove infected panicles",
            "Apply Propiconazole fungicide"
        ],
        "prevention": [
            "Avoid excess nitrogen",
            "Use resistant varieties"
        ]
    },

    "Healthy": {
        "symptoms": [],
        "treatment": [],
        "prevention": [
            "Maintain proper irrigation",
            "Balanced fertilizer use",
            "Regular field monitoring"
        ]
    },

    "Leaf Smut": {
        "symptoms": [
            "Black streaks on leaves",
            "Reduced photosynthesis"
        ],
        "treatment": [
            "Apply suitable fungicide",
            "Remove infected plants"
        ],
        "prevention": [
            "Use disease-free seeds",
            "Crop rotation"
        ]
    },

    "Rice Blast": {
        "symptoms": [
            "Diamond-shaped lesions",
            "Gray centers with brown margins"
        ],
        "treatment": [
            "Spray Tricyclazole",
            "Maintain proper water levels"
        ],
        "prevention": [
            "Use blast-resistant varieties",
            "Avoid excess nitrogen"
        ]
    },

    "Stem Rot": {
        "symptoms": [
            "Rotting of stem base",
            "Wilting of plants"
        ],
        "treatment": [
            "Improve drainage",
            "Apply recommended fungicide"
        ],
        "prevention": [
            "Avoid waterlogging",
            "Balanced fertilization"
        ]
    },

    "Tungro": {
        "symptoms": [
            "Yellow-orange discoloration",
            "Stunted growth"
        ],
        "treatment": [
            "Remove infected plants",
            "Control leafhopper vectors"
        ],
        "prevention": [
            "Vector control",
            "Use resistant varieties"
        ]
    }
}

# =====================================================
# PREDICTION FUNCTION
# =====================================================
def predict_disease(image_path: str):
    filename = os.path.basename(image_path)

    # 🔥 SAME SETTINGS AS COLAB (VERY IMPORTANT)
    results = model(
        image_path,
        imgsz=640,
        conf=0.5,
        iou=0.5,
        device="cpu"   # change to "cuda" later if GPU server
    )[0]

    # =================================================
    # NO DETECTION → HEALTHY
    # =================================================
    if results.boxes is None or len(results.boxes) == 0:
        return {
            "disease": "Healthy",
            "confidence": 99.0,
            "severity": "None",
            "description": "No disease detected.",
            "symptoms": [],
            "treatment": [],
            "prevention": DISEASE_INFO["Healthy"]["prevention"],
            "original_image": f"/uploads/{filename}",
            "result_image": f"/uploads/{filename}"
        }

    # =================================================
    # BEST CONFIDENCE BOX
    # =================================================
    best_idx = int(results.boxes.conf.argmax())
    cls_id = int(results.boxes.cls[best_idx])

    confidence = float(results.boxes.conf[best_idx]) * 100

    # 🔥 NORMALIZE CLASS NAME (CRITICAL FIX)
    disease = results.names[cls_id].strip().title()

    # =================================================
    # SAVE RESULT IMAGE WITH BOUNDING BOX
    # =================================================
    plotted_img = results.plot()
    result_filename = f"result_{filename}"
    result_path = os.path.join(RESULT_DIR, result_filename)
    cv2.imwrite(result_path, plotted_img)

    info = DISEASE_INFO.get(disease, {
        "symptoms": ["Information not available"],
        "treatment": ["Consult agriculture expert"],
        "prevention": ["General crop care recommended"]
    })

    # =================================================
    # SEVERITY CALCULATION
    # =================================================
    severity = (
        "Severe" if confidence >= 95 else
        "Moderate" if confidence >= 85 else
        "Mild"
    )

    return {
        "disease": disease,
        "confidence": round(confidence, 2),
        "severity": severity,
        "description": f"{disease} detected on rice leaf.",
        "symptoms": info["symptoms"],
        "treatment": info["treatment"],
        "prevention": info["prevention"],
        "original_image": f"/uploads/{filename}",
        "result_image": f"/uploads/results/{result_filename}"
    }
