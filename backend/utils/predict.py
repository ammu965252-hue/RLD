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
# LOAD MODEL (LAZY LOADING)
# =====================================================
model = None

def get_model():
    global model
    if model is None:
        print("🔄 Loading YOLO model...")
        model = YOLO(MODEL_PATH)
        print("✅ Model loaded successfully!")
    return model

# =====================================================
# DISEASE INFO (ALL CLASSES + ALL SEVERITY LEVELS)
# =====================================================
DISEASE_INFO = {

    "Healthy": {
        "None": {
            "symptoms": [],
            "treatment": [],
            "prevention": [
                "Maintain proper irrigation",
                "Balanced fertilizer usage",
                "Regular crop monitoring",
                "Good field hygiene"
            ]
        }
    },

    "Rice Blast": {
        "Mild": {
            "symptoms": [
                "Small diamond-shaped lesions",
                "Grey centers on leaves",
                "Limited spread",
                "Normal plant vigor"
            ],
            "treatment": [
                "Monitor disease progression",
                "Preventive fungicide spray",
                "Avoid excess nitrogen",
                "Improve drainage"
            ],
            "prevention": [
                "Use resistant varieties",
                "Balanced fertilization",
                "Proper plant spacing",
                "Routine field inspection"
            ]
        },
        "Moderate": {
            "symptoms": [
                "Larger lesions on multiple leaves",
                "Leaf tip drying",
                "Reduced photosynthesis",
                "Moderate yield loss"
            ],
            "treatment": [
                "Spray Tricyclazole",
                "Maintain standing water",
                "Remove infected plants",
                "Apply potassium fertilizer"
            ],
            "prevention": [
                "Seed treatment",
                "Crop rotation",
                "Avoid dense planting",
                "Timely sowing"
            ]
        },
        "Severe": {
            "symptoms": [
                "Neck blast infection",
                "Panicle breakage",
                "Severe stunting",
                "High yield loss"
            ],
            "treatment": [
                "Immediate fungicide spraying",
                "Multiple spray schedule",
                "Destroy severely infected crop",
                "Consult agriculture expert"
            ],
            "prevention": [
                "Blast-resistant hybrids",
                "Strict nitrogen control",
                "Field sanitation",
                "Avoid infected fields"
            ]
        }
    },

    "Blight": {
        "Mild": {
            "symptoms": [
                "Light yellow streaks",
                "Minor leaf wilting",
                "Small water-soaked lesions",
                "Normal tillering"
            ],
            "treatment": [
                "Monitor spread",
                "Remove infected leaves",
                "Improve drainage",
                "Avoid excess nitrogen"
            ],
            "prevention": [
                "Certified seeds",
                "Balanced nutrition",
                "Proper spacing",
                "Crop rotation"
            ]
        },
        "Moderate": {
            "symptoms": [
                "Extended yellow-orange streaks",
                "Leaf rolling",
                "Reduced tillers",
                "Yield reduction"
            ],
            "treatment": [
                "Copper-based bactericide",
                "Remove infected plants",
                "Improve water management",
                "Reduce nitrogen input"
            ],
            "prevention": [
                "Resistant varieties",
                "Field sanitation",
                "Weed control",
                "Seed treatment"
            ]
        },
        "Severe": {
            "symptoms": [
                "Complete leaf drying",
                "Severe wilting",
                "Panicle sterility",
                "Major yield loss"
            ],
            "treatment": [
                "Immediate bactericide application",
                "Destroy infected crop",
                "Prevent further spread",
                "Expert consultation"
            ],
            "prevention": [
                "Disease-free seeds",
                "Avoid contaminated irrigation",
                "Strict field hygiene",
                "Crop rotation"
            ]
        }
    },

    "Brown Spot": {
        "Mild": {
            "symptoms": [
                "Small brown spots",
                "Yellow halos",
                "No grain impact",
                "Normal growth"
            ],
            "treatment": [
                "Improve soil nutrition",
                "Light fungicide spray",
                "Monitor field",
                "Avoid moisture stress"
            ],
            "prevention": [
                "Balanced fertilization",
                "Seed treatment",
                "Good drainage",
                "Healthy seedlings"
            ]
        },
        "Moderate": {
            "symptoms": [
                "Larger circular lesions",
                "Leaf drying at tips",
                "Reduced grain quality",
                "Yield reduction"
            ],
            "treatment": [
                "Spray Mancozeb",
                "Correct nutrient deficiency",
                "Remove infected leaves",
                "Improve irrigation"
            ],
            "prevention": [
                "Resistant varieties",
                "Crop rotation",
                "Soil health management",
                "Regular monitoring"
            ]
        },
        "Severe": {
            "symptoms": [
                "Heavy leaf spotting",
                "Complete leaf drying",
                "Poor grain filling",
                "Severe yield loss"
            ],
            "treatment": [
                "Immediate fungicide spraying",
                "Remove infected plants",
                "Soil correction",
                "Expert advice"
            ],
            "prevention": [
                "Balanced soil nutrients",
                "Seed treatment",
                "Avoid drought stress",
                "Field sanitation"
            ]
        }
    },

    "False Smut": {
        "Mild": {
            "symptoms": [
                "Few green smut balls",
                "Limited panicle infection",
                "Normal grain formation",
                "No yield impact"
            ],
            "treatment": [
                "Field monitoring",
                "Avoid excess nitrogen",
                "Improve aeration",
                "No immediate chemical spray"
            ],
            "prevention": [
                "Disease-free seeds",
                "Balanced fertilization",
                "Proper drainage",
                "Timely sowing"
            ]
        },
        "Moderate": {
            "symptoms": [
                "Yellow smut balls",
                "Multiple panicles affected",
                "Partial grain replacement",
                "Yield reduction"
            ],
            "treatment": [
                "Spray Propiconazole",
                "Remove infected panicles",
                "Reduce nitrogen",
                "Improve spacing"
            ],
            "prevention": [
                "Crop rotation",
                "Resistant varieties",
                "Field sanitation",
                "Timely planting"
            ]
        },
        "Severe": {
            "symptoms": [
                "Black smut balls",
                "Most panicles infected",
                "Grain completely replaced",
                "Severe yield loss"
            ],
            "treatment": [
                "Immediate fungicide spray",
                "Destroy infected crop",
                "Multiple spray cycles",
                "Expert consultation"
            ],
            "prevention": [
                "Resistant hybrids",
                "Strict nitrogen control",
                "Deep ploughing",
                "Avoid infected fields"
            ]
        }
    },

    "Leaf Smut": {
        "Mild": {
            "symptoms": [
                "Small black streaks",
                "Limited spread",
                "Leaves mostly green",
                "Normal growth"
            ],
            "treatment": [
                "Monitor disease",
                "Remove affected leaves",
                "Light fungicide spray",
                "Improve airflow"
            ],
            "prevention": [
                "Disease-free seeds",
                "Balanced nutrition",
                "Proper irrigation",
                "Field inspection"
            ]
        },
        "Moderate": {
            "symptoms": [
                "Increased black streaks",
                "Partial leaf drying",
                "Reduced photosynthesis",
                "Yield reduction"
            ],
            "treatment": [
                "Apply fungicide",
                "Remove infected plants",
                "Improve drainage",
                "Reduce humidity"
            ],
            "prevention": [
                "Seed treatment",
                "Crop rotation",
                "Soil health management",
                "Regular monitoring"
            ]
        },
        "Severe": {
            "symptoms": [
                "Heavy black streaks",
                "Complete leaf drying",
                "Stunted growth",
                "Severe yield loss"
            ],
            "treatment": [
                "Immediate fungicide spray",
                "Remove infected crop",
                "Field sanitation",
                "Expert advice"
            ],
            "prevention": [
                "Resistant varieties",
                "Strict crop rotation",
                "Avoid infected fields",
                "Residue management"
            ]
        }
    },

    "Stem Rot": {
        "Mild": {
            "symptoms": [
                "Minor stem discoloration",
                "Small lesions at base",
                "Plants upright",
                "No lodging"
            ],
            "treatment": [
                "Improve drainage",
                "Avoid waterlogging",
                "Monitor plants",
                "Preventive fungicide"
            ],
            "prevention": [
                "Balanced fertilization",
                "Proper irrigation",
                "Crop rotation",
                "Field leveling"
            ]
        },
        "Moderate": {
            "symptoms": [
                "Stem base rotting",
                "Lower leaf yellowing",
                "Partial lodging",
                "Reduced tillering"
            ],
            "treatment": [
                "Apply fungicide",
                "Improve aeration",
                "Remove infected plants",
                "Drain excess water"
            ],
            "prevention": [
                "Resistant varieties",
                "Organic matter control",
                "Soil health improvement",
                "Water management"
            ]
        },
        "Severe": {
            "symptoms": [
                "Complete stem collapse",
                "Severe lodging",
                "Root decay",
                "Major yield loss"
            ],
            "treatment": [
                "Immediate fungicide",
                "Remove crop",
                "Field drying",
                "Expert consultation"
            ],
            "prevention": [
                "Avoid continuous rice",
                "Crop residue removal",
                "Deep ploughing",
                "Strict water control"
            ]
        }
    },

    "Tungro": {
        "Mild": {
            "symptoms": [
                "Light yellowing",
                "Slight stunting",
                "Few plants affected",
                "No yield loss"
            ],
            "treatment": [
                "Monitor vectors",
                "Remove infected plants",
                "Light insecticide spray",
                "Improve nutrition"
            ],
            "prevention": [
                "Resistant varieties",
                "Weed control",
                "Timely planting",
                "Vector monitoring"
            ]
        },
        "Moderate": {
            "symptoms": [
                "Yellow-orange leaves",
                "Reduced tillering",
                "Moderate stunting",
                "Field spread"
            ],
            "treatment": [
                "Apply systemic insecticide",
                "Remove infected clumps",
                "Control vectors",
                "Correct nutrients"
            ],
            "prevention": [
                "Synchronised planting",
                "Seedling protection",
                "Vector control",
                "Field sanitation"
            ]
        },
        "Severe": {
            "symptoms": [
                "Severe yellowing",
                "Extreme stunting",
                "Almost no grain",
                "Crop failure risk"
            ],
            "treatment": [
                "Immediate vector control",
                "Destroy infected crop",
                "Field quarantine",
                "Expert guidance"
            ],
            "prevention": [
                "Strict vector management",
                "Resistant cultivars",
                "Crop rotation",
                "Avoid infected nurseries"
            ]
        }
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

    # Get model (lazy loading)
    model = get_model()

    results = model(
        image_path,
        imgsz=640,
        conf=0.1,
        iou=0.5,
        device="cpu"
    )[0]

    # ================= NO DETECTION =================
    if results.boxes is None or len(results.boxes) == 0:
        response = {
            "disease": "Healthy",
            "confidence": 99.0,
            "severity": "None",
            "lesion_count": 0,
            "description": "Healthy rice leaf detected.",
            "symptoms": [],
            "treatment": [],
            "prevention": DISEASE_INFO["Healthy"]["None"]["prevention"],
            "original_image": f"/uploads/{filename}",
            "result_image": f"/uploads/{filename}",
            "timestamp": datetime.now().isoformat()
        }
        save_history(response)
        return response

    # ================= BOX & CLASS =================
    box_count = len(results.boxes)
    best_idx = int(results.boxes.conf.argmax())
    cls_id = int(results.boxes.cls[best_idx])
    confidence = float(results.boxes.conf[best_idx]) * 100
    disease = results.names[cls_id].strip().title()

    # ================= SEVERITY (CVRD) =================
    if box_count >= 7:
        severity = "Severe"
    elif box_count >= 3:
        severity = "Moderate"
    else:
        severity = "Mild"

    # ================= SAVE IMAGE =================
    plotted_img = results.plot()
    result_filename = f"result_{filename}"
    cv2.imwrite(os.path.join(RESULT_DIR, result_filename), plotted_img)

    info = DISEASE_INFO.get(disease, {}).get(severity, {
        "symptoms": ["Information not available"],
        "treatment": ["Consult agriculture expert"],
        "prevention": ["General crop care recommended"]
    })

    response = {
        "disease": disease,
        "confidence": round(confidence, 2),
        "severity": severity,
        "lesion_count": box_count,
        "description": f"{disease} detected with {severity} severity.",
        "symptoms": info["symptoms"],
        "treatment": info["treatment"],
        "prevention": info["prevention"],
        "original_image": f"/uploads/{filename}",
        "result_image": f"/uploads/results/{result_filename}",
        "timestamp": datetime.now().isoformat()
    }

    save_history(response)
    return response
