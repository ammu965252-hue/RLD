import os
import cv2
from ultralytics import YOLO

# ================= LOAD MODEL =================
model = YOLO("model/best.pt")

# ================= OUTPUT DIR =================
RESULT_DIR = "uploads/results"
os.makedirs(RESULT_DIR, exist_ok=True)

# ================= DISEASE INFO =================
# ⚠️ MUST MATCH data.yaml EXACTLY
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

    "Brown spot": {
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

    "Rice blast": {
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

# ================= PREDICTION FUNCTION =================
def predict_disease(image_path: str):
    results = model(image_path)[0]

    # ================= NO DETECTION =================
    if results.boxes is None or len(results.boxes) == 0:
        return {
            "disease": "Unknown",
            "confidence": 0.0,
            "severity": "None",
            "description": "No disease detected.",
            "symptoms": [],
            "treatment": [],
            "prevention": [],
            "result_image": None
        }

    # ================= BEST CONFIDENCE BOX =================
    best_idx = int(results.boxes.conf.argmax())
    cls_id = int(results.boxes.cls[best_idx])
    confidence = float(results.boxes.conf[best_idx]) * 100
    disease = results.names[cls_id]

    # ================= SAVE BOUNDING BOX IMAGE =================
    plotted_img = results.plot()
    filename = f"result_{os.path.basename(image_path)}"
    save_path = os.path.join(RESULT_DIR, filename)
    cv2.imwrite(save_path, plotted_img)

    info = DISEASE_INFO.get(disease, {
        "symptoms": ["Information not available"],
        "treatment": ["Consult agriculture expert"],
        "prevention": ["General crop care recommended"]
    })

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
        "result_image": f"/uploads/results/{filename}"
    }
