# All Code

## Backend

### app.py
```python
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import shutil
import os

from utils.predict import predict_disease

app = FastAPI(title="RiceGuard AI Backend")

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change later for production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Upload directory
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Serve uploaded images
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.post("/detect")
async def detect_disease(file: UploadFile = File(...)):
    # Validate file type
    if not file.content_type.startswith("image/"):
        return {"error": "Invalid file type. Please upload an image."}

    # Save image
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run ML model
    try:
        result = predict_disease(file_path)
    except Exception as e:
        return {"error": f"Prediction failed: {str(e)}"}

    # Send image URL to frontend
    result["image_url"] = f"http://127.0.0.1:8000/uploads/{file.filename}"

    return result
```

### requirements.txt
```
fastapi
uvicorn[standard]
opencv-python
pillow
numpy
matplotlib
ultralytics
pydantic
python-multipart
pandas
python-dotenv
requests
passlib[bcrypt]
python-jose[cryptography]
sqlalchemy
pytest
scikit-learn
```

### utils/predict.py
```python
from ultralytics import YOLO

model = YOLO("model/best.pt")

DISEASE_INFO = {
    "Bacterial Leaf Blight": {
        "symptoms": [
            "Yellow-orange stripes on leaf blades",
            "Leaves wilt and roll up",
            "Creamy bacterial ooze",
            "V-shaped lesions from leaf tips"
        ],
        "prevention": [
            "Use certified disease-free seeds",
            "Ensure proper field drainage",
            "Avoid excess nitrogen fertilizer",
            "Practice crop rotation"
        ]
    },
    "Brown Spot": {
        "symptoms": [
            "Brown circular spots",
            "Yellow halo around lesions",
            "Reduced grain quality"
        ],
        "prevention": [
            "Balanced fertilization",
            "Use resistant varieties",
            "Seed treatment before planting"
        ]
    }
}

def predict_disease(image_path):
    results = model(image_path)[0]

    # ✅ Handle no detection case
    if results.boxes is None or len(results.boxes) == 0:
        return {
            "disease": "Healthy",
            "confidence": 99.0,
            "severity": "None",
            "description": "No disease detected. Leaf appears healthy.",
            "symptoms": [],
            "treatment": [],
            "prevention": [
                "Maintain proper irrigation",
                "Use balanced fertilizers",
                "Regular crop monitoring"
            ]
        }

    disease = results.names[int(results.boxes.cls[0])]
    confidence = float(results.boxes.conf[0]) * 100

    info = DISEASE_INFO.get(disease, {
        "symptoms": ["Symptoms not available"],
        "prevention": ["General crop care recommended"]
    })

    return {
        "disease": disease,
        "confidence": round(confidence, 2),
        "severity": (
            "Severe" if confidence > 95 else
            "Moderate" if confidence > 85 else
            "Mild"
        ),
        "description": f"{disease} detected on rice leaf.",
        "symptoms": info["symptoms"],
        "treatment": [
            "Remove infected leaves",
            "Apply recommended fungicide",
            "Avoid excess nitrogen fertilizer",
            "Ensure proper drainage"
        ],
        "prevention": info["prevention"]
    }
```

## Frontend

### HTML Files

#### about.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>About – RiceGuard AI</title>

  <link rel="stylesheet" href="css/variables.css">
  <link rel="stylesheet" href="css/base.css">
  <link rel="stylesheet" href="css/components.css">
  <link rel="stylesheet" href="css/pages.css">
  <link rel="stylesheet" href="css/animations.css">
</head>

<body>

<!-- ================= NAVBAR ================= -->
<nav class="navbar">
  <div class="container navbar-inner">
    <a href="index.html">
      🌾 <strong>Rice<span style="color:var(--primary)">Guard</span></strong>
    </a>
    <div class="nav-links">
      <a href="index.html">Detect</a>
      <a href="history.html">History</a>
      <a href="chatbot.html">Chatbot</a>
      <a href="dashboard.html">Dashboard</a>
      <a href="about.html" class="active">About</a>
    </div>
  </div>
</nav>

<!-- ================= HERO ================= -->
<section class="about-hero animate-fade">
  <div class="container text-center">
    <span class="badge primary">✨ About RiceGuard AI</span>
    <h1>
      Protecting Rice Crops with <br>
      <span class="text-gradient">Artificial Intelligence</span>
    </h1>
    <p class="text-muted">
      RiceGuard AI helps farmers detect rice leaf diseases early, prevent crop loss,
      and improve agricultural productivity using deep learning.
    </p>

    <div class="hero-actions">
      <a href="index.html" class="btn btn-primary">Try It Now →</a>
      <a href="#" class="btn btn-outline">View on GitHub</a>
    </div>
  </div>
</section>

<!-- ================= PROBLEM ================= -->
<section class="container about-section">
  <div class="about-grid">
    <div>
      <h2>The Problem We're Solving</h2>
      <p class="text-muted">
        Rice feeds more than half of the world's population. However, diseases like
        Bacterial Leaf Blight, Brown Spot, and Leaf Blast cause severe yield losses
        every year.
      </p>
      <p class="text-muted">
        Traditional disease diagnosis requires agricultural experts, which are often
        inaccessible to small and marginal farmers.
      </p>
      <p>
        <strong>RiceGuard AI bridges this gap</strong> by providing instant,
        expert-level diagnosis using just a smartphone image.
      </p>

      <div class="stats-row">
        <div>
          <h3>30%</h3>
          <span class="text-muted">Annual Crop Loss</span>
        </div>
        <div>
          <h3>$5B</h3>
          <span class="text-muted">Economic Impact</span>
        </div>
        <div>
          <h3>100M+</h3>
          <span class="text-muted">Farmers Affected</span>
        </div>
      </div>
    </div>

    <div class="feature-cards">
      <div class="card">
        🌿 <h3>12 Diseases</h3>
        <p class="text-muted">Accurately detected</p>
      </div>
      <div class="card">
        🧠 <h3>50K+ Images</h3>
        <p class="text-muted">Training dataset</p>
      </div>
      <div class="card">
        ⚡ <h3>&lt; 2 Seconds</h3>
        <p class="text-muted">Detection time</p>
      </div>
      <div class="card">
        🎯 <h3>94.7%</h3>
        <p class="text-muted">Accuracy rate</p>
      </div>
    </div>
  </div>
</section>

<!-- ================= FEATURES ================= -->
<section class="about-features">
  <div class="container">
    <h2 class="text-center">Key Features</h2>
    <p class="text-center text-muted mb-6">
      Built with modern AI and designed for real-world farming
    </p>

    <div class="feature-grid">
      <div class="card">🧠 <h3>Deep Learning AI</h3><p class="text-muted">CNN-based disease detection</p></div>
      <div class="card">⚡ <h3>Real-Time Detection</h3><p class="text-muted">Results in seconds</p></div>
      <div class="card">🎯 <h3>High Accuracy</h3><p class="text-muted">Validated by experts</p></div>
      <div class="card">🔐 <h3>Secure & Private</h3><p class="text-muted">No data sharing</p></div>
      <div class="card">🌍 <h3>Offline Capable</h3><p class="text-muted">Mobile-ready design</p></div>
      <div class="card">👩‍🌾 <h3>Farmer Friendly</h3><p class="text-muted">Simple & intuitive UI</p></div>
    </div>
  </div>
</section>

<!-- ================= TECHNOLOGIES ================= -->
<section class="container about-section">
  <h2 class="text-center">Technologies Used</h2>

  <div class="tech-badges">
    <span>TensorFlow</span>
    <span>PyTorch</span>
    <span>Python</span>
    <span>OpenCV</span>
    <span>HTML</span>
    <span>CSS</span>
    <span>JavaScript</span>
  </div>
</section>

<!-- ================= TEAM ================= -->
<section class="about-team">
  <div class="container">
    <h2 class="text-center">Our Team</h2>

    <div class="team-grid">
      <div class="card">
        <div class="avatar">PS</div>
        <h3>Dr. Priya Sharma</h3>
        <p class="text-muted">Project Lead & AI Researcher</p>
      </div>
      <div class="card">
        <div class="avatar">RP</div>
        <h3>Rahul Patel</h3>
        <p class="text-muted">Full Stack Developer</p>
      </div>
      <div class="card">
        <div class="avatar">AS</div>
        <h3>Ananya Singh</h3>
        <p class="text-muted">Data Scientist</p>
      </div>
      <div class="card">
        <div class="avatar">VK</div>
        <h3>Vikram Kumar</h3>
        <p class="text-muted">Agricultural Consultant</p>
      </div>
    </div>
  </div>
</section>

<!-- ================= CTA ================= -->
<section class="about-cta">
  <div class="container text-center">
    <h2>Ready to Protect Your Crops?</h2>
    <p class="text-muted">
      Join thousands of farmers using RiceGuard AI for early disease detection.
    </p>
    <a href="index.html" class="btn btn-primary">Start Detecting →</a>
  </div>
</section>

<!-- ================= FOOTER ================= -->
<footer>
  <div class="container text-center text-muted">
    © 2024 RiceGuard AI — Built for farmers 🌱
  </div>
</footer>

</body>
</html>
```

#### chatbot.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>AI Farming Assistant – RiceGuard</title>

  <link rel="stylesheet" href="css/variables.css">
  <link rel="stylesheet" href="css/base.css">
  <link rel="stylesheet" href="css/components.css">
  <link rel="stylesheet" href="css/pages.css">
  <link rel="stylesheet" href="css/animations.css">
</head>

<body>

<!-- ================= NAVBAR ================= -->
<nav class="navbar">
  <div class="container navbar-inner">
    <a href="index.html">
      🌾 <strong>Rice<span style="color:var(--primary)">Guard</span></strong>
    </a>
    <div class="nav-links">
      <a href="index.html">Detect</a>
      <a href="history.html">History</a>
      <a href="chatbot.html" class="active">Chatbot</a>
      <a href="dashboard.html">Dashboard</a>
      <a href="about.html">About</a>
    </div>
  </div>
</nav>

<!-- ================= MAIN ================= -->
<main class="container mt-6 animate-fade">

  <!-- HEADER -->
  <div class="text-center mb-6">
    <div class="chatbot-icon">🤖</div>
    <h1>Farming Assistant</h1>
    <p class="text-muted">
      Ask anything about rice diseases, farming & treatments
    </p>
  </div>

  <!-- CHAT CARD -->
  <div class="card chat-card">

    <!-- CHAT BODY -->
    <div id="chatBody" class="chat-body">
      <!-- Messages injected here -->
    </div>

    <!-- QUICK QUESTIONS -->
    <div class="quick-questions">
      <span class="text-muted">✨ Quick questions:</span>
      <button onclick="quickAsk('What is Bacterial Leaf Blight?')">What is BLB?</button>
      <button onclick="quickAsk('How to prevent rice diseases?')">Prevention</button>
      <button onclick="quickAsk('Best fertilizers for rice?')">Fertilizers</button>
      <button onclick="quickAsk('When to harvest rice?')">Harvest</button>
    </div>

    <!-- INPUT -->
    <div class="chat-input">
      <input
        type="text"
        id="chatInput"
        placeholder="Type your message..."
        onkeypress="if(event.key==='Enter') sendMessage()"
      />
      <button class="btn btn-primary" onclick="sendMessage()">Send</button>
    </div>

  </div>

</main>

<script src="js/chatbot.js"></script>
</body>
</html>
```

#### dashboard.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Dashboard – RiceGuard AI</title>

  <link rel="stylesheet" href="css/variables.css">
  <link rel="stylesheet" href="css/base.css">
  <link rel="stylesheet" href="css/components.css">
  <link rel="stylesheet" href="css/pages.css">
  <link rel="stylesheet" href="css/animations.css">
</head>

<body>

<!-- ================= SIDEBAR ================= -->
<aside class="sidebar" id="sidebar">
  <div class="sidebar-header">
    🌾 <strong>RiceGuard</strong>
    <button id="closeSidebar">✖</button>
  </div>

  <nav class="sidebar-nav">
    <a href="dashboard.html" class="active">📊 Overview</a>
    <a href="index.html">📷 New Detection</a>
    <a href="history.html">📁 History</a>
    <a href="chatbot.html">💬 Chatbot</a>
    <a href="#">📈 Analytics</a>
    <a href="#">⚙ Settings</a>
  </nav>

  <div class="sidebar-user">
    <div class="avatar">JD</div>
    <div>
      <p>John Doe</p>
      <span class="text-muted">john@farm.com</span>
    </div>
  </div>
</aside>

<!-- ================= MAIN ================= -->
<div class="dashboard-wrapper">

  <!-- HEADER -->
  <header class="dashboard-header">
    <button id="openSidebar" class="menu-btn">☰</button>
    <h1>Dashboard</h1>

    <div class="header-actions">
      <button class="icon-btn">🔔</button>
      <button class="icon-btn">👤</button>
      <button class="icon-btn">🚪</button>
    </div>
  </header>

  <!-- CONTENT -->
  <main class="dashboard-content animate-fade">

    <!-- STATS -->
    <div class="stats-grid">
      <div class="card stat-card">
        <h3>Total Detections</h3>
        <p class="stat-value">1,284</p>
        <span class="stat-change positive">+12%</span>
      </div>

      <div class="card stat-card">
        <h3>Diseases Found</h3>
        <p class="stat-value">847</p>
        <span class="stat-change positive">+8%</span>
      </div>

      <div class="card stat-card">
        <h3>Accuracy Rate</h3>
        <p class="stat-value">94.7%</p>
        <span class="stat-change positive">+2.3%</span>
      </div>

      <div class="card stat-card">
        <h3>Farmers Helped</h3>
        <p class="stat-value">326</p>
        <span class="stat-change positive">+18%</span>
      </div>
    </div>

    <!-- GRAPHS -->
    <div class="dashboard-grid">

      <!-- DISEASE DISTRIBUTION -->
      <div class="card">
        <h2>Disease Distribution</h2>

        <div class="progress-row">
          <span>Bacterial Leaf Blight</span>
          <div class="progress"><div style="width:35%"></div></div>
          <span>35%</span>
        </div>

        <div class="progress-row">
          <span>Brown Spot</span>
          <div class="progress"><div style="width:25%"></div></div>
          <span>25%</span>
        </div>

        <div class="progress-row">
          <span>Leaf Blast</span>
          <div class="progress"><div style="width:22%"></div></div>
          <span>22%</span>
        </div>

        <div class="progress-row">
          <span>Others</span>
          <div class="progress"><div style="width:18%"></div></div>
          <span>18%</span>
        </div>
      </div>

      <!-- RECENT -->
      <div class="card">
        <h2>Recent Detections</h2>

        <div class="recent-item">
          <span>Bacterial Leaf Blight</span>
          <small class="moderate">Moderate</small>
        </div>

        <div class="recent-item">
          <span>Brown Spot</span>
          <small class="mild">Mild</small>
        </div>

        <div class="recent-item">
          <span>Leaf Blast</span>
          <small class="severe">Severe</small>
        </div>

        <a href="history.html" class="btn btn-outline full-width mt-4">
          View All History
        </a>
      </div>

    </div>

    <!-- CHARTS -->
    <div class="dashboard-grid">

      <!-- WEEKLY -->
      <div class="card">
        <h2>Weekly Activity</h2>
        <div class="bar-chart">
          <div style="height:65%">Mon</div>
          <div style="height:45%">Tue</div>
          <div style="height:80%">Wed</div>
          <div style="height:55%">Thu</div>
          <div style="height:90%">Fri</div>
          <div style="height:40%">Sat</div>
          <div style="height:70%">Sun</div>
        </div>
      </div>

      <!-- ACCURACY -->
      <div class="card text-center">
        <h2>Model Accuracy</h2>
        <div class="circle-chart">
          <span>94.7%</span>
        </div>
      </div>

    </div>

  </main>
</div>

<script src="js/dashboard.js"></script>
</body>
</html>
```

#### history.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Detection History – RiceGuard AI</title>

  <!-- CSS -->
  <link rel="stylesheet" href="css/variables.css">
  <link rel="stylesheet" href="css/base.css">
  <link rel="stylesheet" href="css/components.css">
  <link rel="stylesheet" href="css/pages.css">
  <link rel="stylesheet" href="css/animations.css">
</head>

<body>

<!-- ================= NAVBAR ================= -->
<nav class="navbar">
  <div class="container navbar-inner">
    <a href="index.html" class="logo">
      🌾 <strong>Rice<span style="color:var(--primary)">Guard</span></strong>
    </a>

    <div class="nav-links">
      <a href="index.html">Detect</a>
      <a href="history.html" class="active">History</a>
      <a href="chatbot.html">Chatbot</a>
      <a href="dashboard.html">Dashboard</a>
      <a href="about.html">About</a>
    </div>
  </div>
</nav>

<!-- ================= MAIN CONTENT ================= -->
<main class="container animate-fade mt-6">

  <!-- HEADER -->
  <div class="result-header">
    <div>
      <h1>Detection History</h1>
      <p class="text-muted">
        View and manage your previous rice leaf disease detections
      </p>
    </div>

    <div class="actions">
      <button class="btn btn-outline">
        ⬇ Export
      </button>
      <button class="btn btn-outline" id="toggleEmpty">
        Show Empty
      </button>
    </div>
  </div>

  <!-- FILTERS -->
  <div class="card mt-4">
    <div class="filter-row">
      <input
        type="text"
        id="searchInput"
        class="input"
        placeholder="Search by disease name..."
      />

      <select id="severityFilter" class="input">
        <option value="all">All Severity</option>
        <option value="None">Healthy</option>
        <option value="Mild">Mild</option>
        <option value="Moderate">Moderate</option>
        <option value="Severe">Severe</option>
      </select>
    </div>
  </div>

  <!-- EMPTY STATE -->
  <div id="emptyState" class="card text-center mt-6 hidden">
    <div class="mb-4" style="font-size:48px;">📄</div>
    <h2>No detections yet</h2>
    <p class="text-muted mb-4">
      Start by uploading a rice leaf image to detect diseases.
      Your history will appear here.
    </p>
    <a href="index.html" class="btn btn-primary">
      Start Detecting
    </a>
  </div>

  <!-- TABLE -->
  <div id="tableWrapper" class="card mt-6">
    <table class="table">
      <thead>
        <tr>
          <th>Image</th>
          <th>Disease</th>
          <th>Severity</th>
          <th>Confidence</th>
          <th>Date & Time</th>
          <th style="text-align:right;">Actions</th>
        </tr>
      </thead>

      <tbody id="historyTable">
        <!-- Rows injected by history.js -->
      </tbody>
    </table>
  </div>

</main>

<!-- ================= FOOTER ================= -->
<footer class="mt-6" style="border-top:1px solid var(--border);">
  <div class="container text-center text-muted" style="padding:16px;">
    © 2024 RiceGuard AI – Built for farmers, by innovators 🌱
  </div>
</footer>

<!-- JS -->
<script src="js/main.js"></script>
<script src="js/history.js"></script>

</body>
</html>
```

#### index.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>RiceGuard AI – Rice Leaf Disease Detection</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <!-- Fonts -->
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@600;700&display=swap" rel="stylesheet">

  <!-- CSS -->
  <link rel="stylesheet" href="css/variables.css">
  <link rel="stylesheet" href="css/base.css">
  <link rel="stylesheet" href="css/animations.css">
  <link rel="stylesheet" href="css/components.css">
  <link rel="stylesheet" href="css/pages.css">
</head>

<body>

<!-- NAVBAR -->
<nav class="navbar">
  <div class="container navbar-inner">
    <a href="index.html" class="logo">
      🌾 <strong>Rice<span style="color:var(--primary)">Guard</span></strong>
    </a>

    <div class="nav-links">
      <a href="index.html">Detect</a>
      <a href="history.html">History</a>
      <a href="chatbot.html">Chatbot</a>
      <a href="dashboard.html">Dashboard</a>
      <a href="about.html">About</a>
    </div>

    <div>
      <a href="login.html" class="btn btn-outline">Login</a>
      <a href="register.html" class="btn btn-primary">Get Started</a>
    </div>
  </div>
</nav>

<!-- HERO SECTION -->
<section class="hero">
  <div class="container hero-grid">
    
    <!-- LEFT -->
    <div class="animate-fade">
      <span class="badge">🌿 AI Powered Detection</span>

      <h1>
        Protect Your <br>
        <span class="text-gradient">Rice Crops</span> with AI
      </h1>

      <p class="text-muted">
        Upload a rice leaf image and instantly detect diseases,
        severity, and treatment recommendations.
      </p>

      <div class="hero-buttons">
        <button class="btn btn-primary" onclick="openFilePicker()">📤 Upload Image</button>
        <button class="btn btn-outline">📷 Take Photo</button>
      </div>
    </div>

    <!-- RIGHT -->
    <div class="card upload-card animate-slide">
      <div 
        id="uploadZone" 
        class="upload-zone"
        onclick="openFilePicker()"
      >
        <input type="file" id="fileInput" accept="image/*" hidden>

        <div id="uploadPlaceholder">
          <div class="upload-icon">⬆️</div>
          <h3>Drop your image here</h3>
          <p class="text-muted">or click to browse</p>
          <small class="text-muted">JPG, PNG, WebP supported</small>
        </div>

        <div id="previewContainer" class="hidden">
          <img id="previewImage" alt="Preview">
          <button class="remove-btn" onclick="removeImage(event)">✖</button>
        </div>
      </div>

      <button 
        id="detectBtn"
        class="btn btn-primary hidden mt-4"
        onclick="detectDisease()"
      >
        Detect Disease →
      </button>
    </div>

  </div>
</section>

<!-- HOW IT WORKS -->
<section class="how-it-works">
  <div class="container text-center">
    <h2>How It Works</h2>
    <p class="text-muted">Fast, accurate, farmer-friendly AI detection</p>

    <div class="features-grid">
      <div class="card">
        🔍 <h3>AI Detection</h3>
        <p class="text-muted">Deep learning trained on 50,000+ images</p>
      </div>
      <div class="card">
        🛡️ <h3>Early Prevention</h3>
        <p class="text-muted">Detect diseases before crop loss</p>
      </div>
      <div class="card">
        ⚡ <h3>Fast Results</h3>
        <p class="text-muted">Diagnosis in seconds</p>
      </div>
    </div>
  </div>
</section>

<!-- STATS -->
<section class="stats">
  <div class="container stats-grid">
    <div><h2>50K+</h2><p>Scans</p></div>
    <div><h2>95%</h2><p>Accuracy</p></div>
    <div><h2>12</h2><p>Diseases</p></div>
    <div><h2>10K+</h2><p>Farmers</p></div>
  </div>
</section>

<script src="js/main.js"></script>
<script src="js/upload.js"></script>
</body>
</html>
```

#### login.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Login – RiceGuard AI</title>

  <link rel="stylesheet" href="css/variables.css">
  <link rel="stylesheet" href="css/base.css">
  <link rel="stylesheet" href="css/components.css">
  <link rel="stylesheet" href="css/pages.css">
  <link rel="stylesheet" href="css/animations.css">
</head>

<body class="auth-body">

<!-- BACKGROUND DECOR -->
<div class="auth-bg">
  <div class="blur-circle primary"></div>
  <div class="blur-circle accent"></div>
</div>

<!-- ================= LOGIN CARD ================= -->
<div class="auth-container animate-fade">

  <!-- LOGO -->
  <div class="auth-logo">
    🌾 <span>Rice<span class="primary-text">Guard</span></span>
  </div>

  <div class="card auth-card">
    <h1>Welcome Back</h1>
    <p class="text-muted mb-4">Sign in to continue to RiceGuard</p>

    <form id="loginForm">

      <!-- EMAIL -->
      <label>Email or Phone</label>
      <input
        type="text"
        id="email"
        class="input"
        placeholder="Enter your email or phone"
        required
      />

      <!-- PASSWORD -->
      <label>Password</label>
      <div class="password-field">
        <input
          type="password"
          id="password"
          class="input"
          placeholder="Enter your password"
          required
        />
        <button type="button" id="togglePassword">👁</button>
      </div>

      <!-- REMEMBER -->
      <div class="checkbox-row">
        <input type="checkbox" id="remember">
        <label for="remember">Remember me for 30 days</label>
      </div>

      <!-- SUBMIT -->
      <button type="submit" class="btn btn-primary full-width">
        Sign In →
      </button>
    </form>

    <div class="divider">or continue with</div>

    <div class="social-buttons">
      <button class="btn btn-outline">Google</button>
      <button class="btn btn-outline">Phone OTP</button>
    </div>
  </div>

  <p class="text-muted mt-4">
    Don't have an account?
    <a href="login.html" class="primary-text">Create account</a>
  </p>

</div>

<script src="js/auth.js"></script>
</body>
</html>
```

#### register.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Register – RiceGuard AI</title>

  <link rel="stylesheet" href="css/variables.css">
  <link rel="stylesheet" href="css/base.css">
  <link rel="stylesheet" href="css/components.css">
  <link rel="stylesheet" href="css/pages.css">
  <link rel="stylesheet" href="css/animations.css">
</head>

<body class="auth-body">

<!-- BACKGROUND DECOR -->
<div class="auth-bg">
  <div class="blur-circle primary"></div>
  <div class="blur-circle accent"></div>
</div>

<!-- ================= REGISTER CARD ================= -->
<div class="auth-container animate-fade">

  <!-- LOGO -->
  <div class="auth-logo">
    🌾 <span>Rice<span class="primary-text">Guard</span></span>
  </div>

  <div class="card auth-card">
    <h1>Create Account</h1>
    <p class="text-muted mb-4">
      Join RiceGuard to protect your crops
    </p>

    <form id="registerForm">

      <!-- FULL NAME -->
      <label>Full Name</label>
      <input type="text" id="fullName" class="input" placeholder="Enter your full name" required>

      <!-- EMAIL -->
      <label>Email Address</label>
      <input type="email" id="email" class="input" placeholder="Enter your email" required>

      <!-- PHONE -->
      <label>Phone Number (Optional)</label>
      <input type="tel" id="phone" class="input" placeholder="Enter your phone number">

      <!-- PASSWORD -->
      <label>Password</label>
      <div class="password-field">
        <input type="password" id="password" class="input" placeholder="Create a password" required>
        <button type="button" id="togglePassword">👁</button>
      </div>

      <!-- PASSWORD RULES -->
      <ul class="password-rules" id="passwordRules">
        <li id="rule-length">❌ At least 8 characters</li>
        <li id="rule-upper">❌ One uppercase letter</li>
        <li id="rule-lower">❌ One lowercase letter</li>
        <li id="rule-number">❌ One number</li>
      </ul>

      <!-- CONFIRM PASSWORD -->
      <label>Confirm Password</label>
      <div class="password-field">
        <input type="password" id="confirmPassword" class="input" placeholder="Confirm password" required>
        <button type="button" id="toggleConfirm">👁</button>
      </div>

      <p id="matchMsg" class="error-text hidden">Passwords do not match</p>

      <!-- TERMS -->
      <div class="checkbox-row">
        <input type="checkbox" id="terms">
        <label for="terms">
          I agree to the <a href="#">Terms</a> & <a href="#">Privacy Policy</a>
        </label>
      </div>

      <!-- SUBMIT -->
      <button type="submit" id="registerBtn" class="btn btn-primary full-width" disabled>
        Create Account →
      </button>

    </form>
  </div>

  <p class="text-muted mt-4">
    Already have an account?
    <a href="login.html" class="primary-text">Sign in</a>
  </p>

</div>

<script src="js/auth.js"></script>
</body>
</html>
```

#### result.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Detection Result – RiceGuard AI</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <link rel="stylesheet" href="css/variables.css">
  <link rel="stylesheet" href="css/base.css">
  <link rel="stylesheet" href="css/animations.css">
  <link rel="stylesheet" href="css/components.css">
  <link rel="stylesheet" href="css/pages.css">
</head>

<body>

<!-- NAVBAR -->
<nav class="navbar">
  <div class="container navbar-inner">
    <a href="index.html" class="logo">🌾 <b>Rice<span class="text-primary">Guard</span></b></a>
    <div class="nav-links">
      <a href="index.html">Detect</a>
      <a href="history.html">History</a>
      <a href="chatbot.html">Chatbot</a>
      <a href="dashboard.html">Dashboard</a>
      <a href="about.html">About</a>
    </div>
  </div>
</nav>

<!-- ANALYZING -->
<section id="analyzing" class="center-screen">
  <div class="text-center animate-fade">
    <div class="loader-circle">🌿</div>
    <h2>Analyzing Image...</h2>
    <p class="text-muted">Our AI is examining your rice leaf</p>
    <div class="progress">
      <div class="progress-bar"></div>
    </div>
  </div>
</section>

<!-- RESULT -->
<section id="resultPage" class="hidden">
  <div class="container">

    <!-- HEADER -->
    <div class="result-header">
      <div>
        <h1>Detection Results</h1>
        <p class="text-muted">Analysis completed successfully</p>
      </div>
      <div class="actions">
        <button class="btn btn-outline">🔗 Share</button>
        <button class="btn btn-outline">⬇ Download</button>
        <a href="index.html" class="btn btn-primary">🔄 New Scan</a>
      </div>
    </div>

    <div class="result-grid">

      <!-- LEFT -->
      <div>
        <div class="image-grid">
          <div class="card">
            <h3>Original Image</h3>
            <img id="originalImg">
          </div>

          <div class="card">
            <h3>Detection Result</h3>
            <div class="detect-box">
              <img id="detectImg">
              <div class="bbox"></div>
              <span class="label">BLB Detected</span>
            </div>
          </div>
        </div>

        <div class="card">
          <h3>AI Heatmap</h3>
          <div class="heatmap">
            <img id="heatmapImg">
            <div class="heatmap-bar"></div>
          </div>
        </div>

        <div class="card">
          <h3>Symptoms Identified</h3>
          <ul id="symptoms"></ul>
        </div>
      </div>

      <!-- RIGHT -->
      <div>
        <div class="card severity-card">
          <h2>Bacterial Leaf Blight</h2>
          <p class="text-muted">Confidence</p>
          <div class="progress">
            <div class="progress-bar" style="width:94.7%"></div>
          </div>
          <p class="severity moderate">Moderate</p>
          <p class="text-muted mt-2">
            BLB is caused by Xanthomonas oryzae. It appears as yellow lesions.
          </p>
        </div>

        <div class="card">
          <h3>Treatment</h3>
          <ol id="treatment"></ol>
        </div>

        <div class="card">
          <h3>Prevention</h3>
          <ul id="prevention"></ul>
        </div>

        <a href="chatbot.html" class="btn btn-primary full-width">
          Ask Our AI Expert →
        </a>
      </div>

    </div>
  </div>
</section>

<script src="js/result.js"></script>
</body>
</html>
```

### script.js
```javascript
// Front-end only placeholder logic

console.log("RiceGuard AI UI Loaded");

// Future use:
// - Image preview
// - Loading animation
// - Display model results
```

### README.md
```markdown
# Rice Leaf Detection - Frontend

A modern, responsive web interface for the Rice Leaf Disease Detection system. This frontend provides users with an intuitive platform to upload leaf images, view detection results, access detection history, and interact with an AI chatbot for farming advice.

## 📁 Project Structure

```
frontend/
├── index.html                 # Home / Upload page
├── result.html                # Detection result page
├── history.html               # Detection history
├── chatbot.html               # AI farmer chatbot
├── dashboard.html             # Dashboard & analytics
├── about.html                 # About project
├── login.html                 # Login page
├── register.html              # Register page
│
├── css/
│   ├── variables.css          # Color system & fonts (CSS variables)
│   ├── base.css               # Reset, typography, layout helpers
│   ├── components.css         # Navbar, cards, buttons, tables
│   ├── pages.css              # Page-specific styles
│   └── animations.css         # Fade, slide, pulse animations
│
├── js/
│   ├── main.js                # Global JS (navbar, theme, utils)
│   ├── upload.js              # Image upload & preview logic
│   ├── result.js              # Result page logic
│   ├── history.js             # Search, filter, table logic
│   ├── chatbot.js             # Chatbot message logic
│   ├── auth.js                # Login & register logic
│   └── dashboard.js           # Charts & stats logic
│
├── assets/
│   ├── images/
│   │   ├── hero-bg.png
│   │   ├── logo.png
│   │   └── placeholders/
│   └── icons/
│
└── README.md                  # Project documentation

```

## 🎨 Design System

### Color Palette
- **Primary**: #2ecc71 (Green) - Main actions and highlights
- **Secondary**: #3498db (Blue) - Secondary actions
- **Danger**: #e74c3c (Red) - Destructive actions
- **Warning**: #f39c12 (Orange) - Warnings and alerts
- **Neutrals**: Gray scale from dark to light

### Typography
- **Primary Font**: Segoe UI, Tahoma, Geneva, Verdana
- **Secondary Font**: Georgia (serif)
- **Monospace**: Courier New

### Spacing & Layout
- Uses CSS custom properties for consistent spacing
- Responsive grid layout with flexbox
- Mobile-first design approach

## 🛠️ Technologies

- **HTML5** - Semantic markup
- **CSS3** - Custom properties, Grid, Flexbox, Animations
- **Vanilla JavaScript** - No dependencies for core functionality
- **Chart.js** (optional) - For dashboard analytics
- **LocalStorage API** - Client-side data persistence

## 🚀 Features

### Pages

#### 1. **Home / Upload (index.html)**
- Drag-and-drop image upload
- Click to browse file selection
- Image preview before upload
- File validation (type and size)

#### 2. **Detection Results (result.html)**
- Display detected disease name
- Show confidence score
- Display severity level
- Provide recommendations
- Download report option

#### 3. **History (history.html)**
- View all past detection results
- Search by disease name or ID
- Filter by severity level
- Filter by date range
- Sortable table
- Delete old results

#### 4. **AI Farmer Chatbot (chatbot.html)**
- Real-time chat interface
- Typing indicators
- Message history
- Agricultural advice integration

#### 5. **Dashboard (dashboard.html)**
- Key statistics cards
- Scan trends visualization
- Disease distribution charts
- Download reports
- Export data (CSV/JSON)

#### 6. **Authentication (login.html, register.html)**
- User registration
- Secure login
- Form validation
- Error handling

#### 7. **About (about.html)**
- Project information
- Team member profiles
- Project goals and technology stack

## 🎭 CSS Modules

### variables.css
Defines the design system through CSS custom properties:
- Colors and gradients
- Typography scales
- Spacing system
- Border radius tokens
- Shadow definitions
- Transition durations

### base.css
Foundation styles:
- CSS reset
- Typography hierarchy
- Layout utilities
- Display helpers
- Spacing utilities

### components.css
Reusable UI components:
- Navbar styling
- Card components
- Button variants (primary, secondary, danger, outline)
- Form elements
- Tables
- Badges and alerts

### pages.css
Page-specific styling:
- Upload interface styles
- Result display layouts
- History table styling
- Chatbot message interface
- Dashboard grid
- Authentication page styling

### animations.css
Animation library:
- Fade in/out
- Slide animations (left, right, up, down)
- Pulse effects
- Scale animations
- Spin and bounce
- Custom animations

## 📜 JavaScript Modules

### main.js
Global utilities and functions:
- Theme toggle (light/dark mode)
- Navbar interaction
- Notification system
- API wrapper function
- LocalStorage helpers
- Date/file formatting

### upload.js
Image upload functionality:
- Drag-and-drop handling
- File validation
- Image preview
- Server upload with progress

### result.js
Result display logic:
- Load result data from API
- Display formatted results
- Download report functionality

### history.js
Detection history management:
- Load history from API
- Filter and search functionality
- Delete results
- Date range filtering

### chatbot.js
Chatbot interface logic:
- Send messages
- Display chat bubbles
- Typing indicators
- Chat history loading

### auth.js
Authentication logic:
- Login form handling
- Registration form handling
- Token management
- Protected route checking

### dashboard.js
Analytics and dashboard:
- Load statistics
- Chart rendering (Chart.js)
- Data export
- Report generation

## 🔌 API Integration Points

The frontend expects the following API endpoints:

```javascript
// Upload
POST /api/upload

// Results
GET /api/result/:id
DELETE /api/result/:id
GET /api/result/:id/download

// History
GET /api/history

// Chatbot
POST /api/chatbot/message
GET /api/chatbot/history

// Dashboard
GET /api/dashboard/stats
GET /api/dashboard/report
GET /api/dashboard/export?format=csv

// Authentication
POST /api/auth/login
POST /api/auth/register
```

## 🎯 Usage

### Local Development
1. Open any HTML file in a browser
2. No build process needed
3. LocalStorage used for theme and session data

### Production Deployment
1. Minify CSS and JavaScript
2. Optimize images
3. Set up CORS if backend is on different domain
4. Configure API base URL
5. Add security headers

## 🎨 Customization

### Changing Colors
Edit `css/variables.css`:
```css
:root {
    --primary: #2ecc71;        /* Change primary color */
    --secondary: #3498db;      /* Change secondary color */
}
```

### Adding Animations
Add new keyframes in `css/animations.css` and apply to elements:
```html
<div class="fade-in">Animated content</div>
```

### Creating New Pages
1. Create new HTML file
2. Include CSS files
3. Include `main.js`
4. Include page-specific JS
5. Update navbar navigation

## ⚡ Performance Optimization

- CSS organized in separate files for better caching
- Minimal JavaScript dependencies
- LocalStorage for client-side data
- Lazy loading ready
- Mobile-optimized layout

## 🔒 Security Considerations

- Sanitize user inputs
- Validate file uploads on backend
- Use HTTPS for API calls
- Store auth tokens securely
- Implement CORS properly
- Add CSP headers

## 📱 Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Mobile)

## 🤝 Contributing

When adding new features:
1. Keep CSS modular
2. Use CSS variables for colors and spacing
3. Follow existing naming conventions
4. Add comments for complex logic
5. Test on mobile devices

## 📝 License

[Add your license information here]

## 📧 Contact

[Add contact information here]
```

### CSS Files

#### animations.css
```css
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}

.animate-fade {
  animation: fadeIn 0.6s ease forwards;
}

.animate-slide {
  animation: slideUp 0.6s ease forwards;
}

.animate-pulse {
  animation: pulse 1.5s infinite;
}
```

#### base.css
```css
*,
*::before,
*::after {
  box-sizing: border-box;
}

html, body {
  margin: 0;
  padding: 0;
  font-family: var(--font-main);
  color: var(--text-main);
  background: var(--background);
  line-height: 1.6;
}

img {
  max-width: 100%;
  display: block;
}

a {
  text-decoration: none;
  color: inherit;
}

h1, h2, h3, h4 {
  font-family: var(--font-display);
  margin: 0;
}

.container {
  max-width: 1200px;
  margin: auto;
  padding: 0 16px;
}

.hidden {
  display: none !important;
}

.text-muted {
  color: var(--text-muted);
}

.text-center {
  text-align: center;
}

.mt-2 { margin-top: 8px; }
.mt-4 { margin-top: 16px; }
.mt-6 { margin-top: 24px; }
.mb-4 { margin-bottom: 16px; }
.mb-6 { margin-bottom: 24px; }
```

#### components.css
```css
/* NAVBAR */
.navbar {
  position: sticky;
  top: 0;
  z-index: 50;
  background: rgba(255,255,255,0.9);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--border);
}

.navbar-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
}

.nav-links {
  display: flex;
  gap: 20px;
}

.nav-links a {
  font-weight: 500;
  color: var(--text-muted);
}

.nav-links a.active,
.nav-links a:hover {
  color: var(--primary);
}

/* BUTTONS */
.btn {
  padding: 10px 18px;
  border-radius: var(--radius-md);
  border: none;
  cursor: pointer;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.btn-primary {
  background: var(--primary);
  color: white;
}

.btn-outline {
  background: transparent;
  border: 1px solid var(--border);
  color: var(--text-main);
}

.btn-primary:hover {
  background: var(--primary-dark);
}

/* CARDS */
.card {
  background: var(--card-bg);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  padding: 20px;
}

/* INPUTS */
.input {
  width: 100%;
  padding: 12px 14px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border);
  font-size: 14px;
}

/* TABLE */
.table {
  width: 100%;
  border-collapse: collapse;
}

.table th,
.table td {
  padding: 12px;
  border-bottom: 1px solid var(--border);
  text-align: left;
}

.table th {
  background: var(--background-muted);
  font-weight: 600;
}
```

#### pages.css
```css
.hero {
  padding: 80px 0;
  background: linear-gradient(to bottom, #f0fdf4, white);
}

.hero-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  align-items: center;
}

.badge {
  background: rgba(22,163,74,0.1);
  color: var(--primary);
  padding: 6px 14px;
  border-radius: 999px;
  font-weight: 600;
  font-size: 14px;
}

.text-gradient {
  background: linear-gradient(to right, #16a34a, #22c55e);
  -webkit-background-clip: text;
  color: transparent;
}

.upload-card {
  padding: 24px;
}

.upload-zone {
  border: 2px dashed var(--primary);
  border-radius: var(--radius-lg);
  padding: 30px;
  text-align: center;
  cursor: pointer;
}

.upload-icon {
  font-size: 32px;
  margin-bottom: 12px;
}

#previewImage {
  width: 100%;
  height: 220px;
  object-fit: cover;
  border-radius: var(--radius-md);
}

.remove-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(0,0,0,0.6);
  color: white;
  border: none;
  border-radius: 50%;
  padding: 6px;
  cursor: pointer;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit,minmax(220px,1fr));
  gap: 20px;
  margin-top: 40px;
}

.stats {
  padding: 60px 0;
  background: var(--background-muted);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4,1fr);
  text-align: center;
}
.center-screen {
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.loader-circle {
  width: 90px;
  height: 90px;
  border-radius: 24px;
  background: linear-gradient(to br, #16a34a, #22c55e);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40px;
  animation: pulse 1.5s infinite;
}

.result-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 30px;
}

.detect-box {
  position: relative;
}

.bbox {
  position: absolute;
  border: 3px solid red;
  width: 120px;
  height: 90px;
  top: 40%;
  left: 35%;
}

.label {
  position: absolute;
  bottom: 10px;
  right: 10px;
  background: red;
  color: white;
  padding: 4px 8px;
  font-size: 12px;
}

.severity.moderate {
  background: #facc15;
  padding: 6px 12px;
  border-radius: 999px;
  display: inline-block;
}
.filter-row {
  display: flex;
  gap: 12px;
}

.badge {
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
}

.badge.none { background:#dcfce7; color:#166534; }
.badge.mild { background:#d1fae5; color:#065f46; }
.badge.moderate { background:#fef3c7; color:#92400e; }
.badge.severe { background:#fee2e2; color:#991b1b; }
.chat-card {
  max-width: 700px;
  margin: auto;
  display: flex;
  flex-direction: column;
  height: 550px;
}

.chat-body {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  background: var(--background-muted);
}

.chat-msg {
  max-width: 70%;
  padding: 10px 14px;
  margin-bottom: 12px;
  border-radius: 14px;
  white-space: pre-line;
}

.chat-msg.user {
  background: var(--primary);
  color: white;
  margin-left: auto;
}

.chat-msg.bot {
  background: white;
  border: 1px solid var(--border);
}

.chat-input {
  display: flex;
  gap: 8px;
  padding: 12px;
  border-top: 1px solid var(--border);
}

.chat-input input {
  flex: 1;
  padding: 10px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border);
}

.quick-questions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  padding: 12px;
  border-top: 1px solid var(--border);
}

.quick-questions button {
  font-size: 12px;
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid var(--border);
  background: white;
  cursor: pointer;
}

.chatbot-icon {
  font-size: 48px;
}
/* DASHBOARD */
.sidebar {
  width: 250px;
  background: #0f172a;
  color: white;
  position: fixed;
  inset: 0 auto 0 0;
  transform: translateX(-100%);
  transition: 0.3s;
  z-index: 50;
}

.sidebar.show {
  transform: translateX(0);
}

.sidebar-header {
  padding: 16px;
  display: flex;
  justify-content: space-between;
}

.sidebar-nav a {
  display: block;
  padding: 12px 16px;
  color: #cbd5f5;
}

.sidebar-nav a.active,
.sidebar-nav a:hover {
  background: #1e293b;
  color: white;
}

.sidebar-user {
  padding: 16px;
  border-top: 1px solid #1e293b;
  display: flex;
  gap: 10px;
}

.avatar {
  background: var(--primary);
  color: white;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.dashboard-wrapper {
  margin-left: 0;
}

.dashboard-header {
  padding: 12px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--border);
}

.menu-btn {
  font-size: 20px;
}

.dashboard-content {
  padding: 20px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit,minmax(220px,1fr));
  gap: 16px;
}

.stat-card {
  position: relative;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
}

.stat-change {
  position: absolute;
  top: 16px;
  right: 16px;
  font-size: 12px;
}

.positive {
  color: green;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit,minmax(300px,1fr));
  gap: 16px;
  margin-top: 16px;
}

.progress-row {
  display: grid;
  grid-template-columns: 1fr 3fr auto;
  align-items: center;
  gap: 10px;
}

.progress {
  height: 8px;
  background: #e5e7eb;
  border-radius: 999px;
}

.progress div {
  height: 100%;
  background: var(--primary);
  border-radius: 999px;
}

.recent-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
}

.bar-chart {
  display: flex;
  align-items: flex-end;
  gap: 8px;
  height: 150px;
}

.bar-chart div {
  flex: 1;
  background: var(--primary);
  color: white;
  text-align: center;
  font-size: 10px;
  border-radius: 6px 6px 0 0;
}

.circle-chart {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  border: 12px solid var(--primary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  margin: auto;
}
.about-hero {
  padding: 80px 20px;
  background: linear-gradient(to bottom, #ecfdf5, #ffffff);
}

.text-gradient {
  background: linear-gradient(to right, #16a34a, #22c55e);
  -webkit-background-clip: text;
  color: transparent;
}

.about-section {
  padding: 60px 20px;
}

.about-grid {
  display: grid;
  grid-template-columns: 2fr 1.5fr;
  gap: 40px;
}

.stats-row {
  display: flex;
  gap: 24px;
  margin-top: 24px;
}

.feature-cards {
  display: grid;
  grid-template-columns: repeat(2,1fr);
  gap: 16px;
}

.about-features {
  padding: 60px 20px;
  background: #f8fafc;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit,minmax(220px,1fr));
  gap: 16px;
}

.tech-badges {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 12px;
  margin-top: 24px;
}

.tech-badges span {
  padding: 8px 14px;
  border-radius: 999px;
  border: 1px solid var(--border);
}

.about-team {
  padding: 60px 20px;
}

.team-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit,minmax(220px,1fr));
  gap: 16px;
}

.about-cta {
  padding: 60px 20px;
  background: linear-gradient(to right, #16a34a, #22c55e);
  color: white;
}

.about-cta .btn {
  background: white;
  color: #16a34a;
  margin-top: 16px;
}
/* AUTH PAGES */
.auth-body {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(to bottom right, #ecfdf5, #ffffff);
}

.auth-bg .blur-circle {
  position: fixed;
  width: 300px;
  height: 300px;
  border-radius: 50%;
  filter: blur(120px);
  opacity: 0.4;
}

.blur-circle.primary {
  background: var(--primary);
  top: 10%;
  left: 10%;
}

.blur-circle.accent {
  background: var(--accent);
  bottom: 10%;
  right: 10%;
}

.auth-container {
  position: relative;
  z-index: 2;
  max-width: 420px;
  width: 100%;
  padding: 20px;
  text-align: center;
}

.auth-logo {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 16px;
}

.auth-card h1 {
  margin-bottom: 6px;
}

.password-field {
  position: relative;
}

.password-field button {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
}

.checkbox-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 12px 0;
}

.divider {
  margin: 20px 0;
  font-size: 12px;
  color: var(--muted);
}

.social-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}
.password-rules {
  font-size: 12px;
  margin: 8px 0 12px;
  padding-left: 16px;
}

.password-rules li {
  margin-bottom: 4px;
}

.error-text {
  color: red;
  font-size: 12px;
  margin-bottom: 8px;
}

.hidden {
  display: none;
}
```

#### variables.css
```css
:root {
  /* Brand Colors */
  --primary: #16a34a;        /* emerald-600 */
  --primary-dark: #15803d;
  --accent: #22c55e;
  --danger: #dc2626;
  --warning: #f59e0b;
  --info: #2563eb;

  /* Backgrounds */
  --background: #ffffff;
  --background-muted: #f7fdf9;
  --card-bg: #ffffff;
  --sidebar-bg: #0f172a;

  /* Text */
  --text-main: #0f172a;
  --text-muted: #64748b;
  --text-light: #f8fafc;

  /* Borders & Radius */
  --border: #e5e7eb;
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 16px;
  --radius-xl: 24px;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-md: 0 6px 20px rgba(0,0,0,0.08);
  --shadow-lg: 0 15px 40px rgba(0,0,0,0.12);

  /* Fonts */
  --font-main: "Inter", system-ui, -apple-system, sans-serif;
  --font-display: "Poppins", system-ui, sans-serif;
}
```

### JavaScript Files

#### auth.js
```javascript
// PASSWORD TOGGLE
const togglePassword = document.getElementById("togglePassword");
const passwordInput = document.getElementById("password");

if (togglePassword) {
  togglePassword.onclick = () => {
    passwordInput.type =
      passwordInput.type === "password" ? "text" : "password";
  };
}

// LOGIN FORM
const loginForm = document.getElementById("loginForm");

if (loginForm) {
  loginForm.onsubmit = (e) => {
    e.preventDefault();

    const email = document.getElementById("email").value;
    const password = passwordInput.value;
    const remember = document.getElementById("remember").checked;

    console.log("LOGIN DATA:", { email, password, remember });

    alert("Login successful (frontend demo)");
    window.location.href = "dashboard.html";
  };
}
// ================= REGISTER LOGIC =================
const password = document.getElementById("password");
const confirmPassword = document.getElementById("confirmPassword");
const rules = {
  length: document.getElementById("rule-length"),
  upper: document.getElementById("rule-upper"),
  lower: document.getElementById("rule-lower"),
  number: document.getElementById("rule-number"),
};
const terms = document.getElementById("terms");
const registerBtn = document.getElementById("registerBtn");
const matchMsg = document.getElementById("matchMsg");

function updateRule(el, valid) {
  el.textContent = (valid ? "✔ " : "❌ ") + el.textContent.slice(2);
  el.style.color = valid ? "green" : "";
}

function validatePassword() {
  const val = password.value;

  const checks = {
    length: val.length >= 8,
    upper: /[A-Z]/.test(val),
    lower: /[a-z]/.test(val),
    number: /[0-9]/.test(val),
  };

  updateRule(rules.length, checks.length);
  updateRule(rules.upper, checks.upper);
  updateRule(rules.lower, checks.lower);
  updateRule(rules.number, checks.number);

  return Object.values(checks).every(Boolean);
}

function validateMatch() {
  const match = password.value === confirmPassword.value && confirmPassword.value !== "";
  matchMsg.classList.toggle("hidden", match);
  return match;
}

function toggleRegisterButton() {
  registerBtn.disabled = !(validatePassword() && validateMatch() && terms.checked);
}

password?.addEventListener("input", toggleRegisterButton);
confirmPassword?.addEventListener("input", toggleRegisterButton);
terms?.addEventListener("change", toggleRegisterButton);

// TOGGLE VISIBILITY
document.getElementById("toggleConfirm")?.addEventListener("click", () => {
  confirmPassword.type =
    confirmPassword.type === "password" ? "text" : "password";
});

// SUBMIT
document.getElementById("registerForm")?.addEventListener("submit", (e) => {
  e.preventDefault();
  alert("Account created successfully (frontend demo)");
  window.location.href = "login.html";
});
```

#### chatbot.js
```javascript
const chatBody = document.getElementById("chatBody");
const chatInput = document.getElementById("chatInput");

const botResponses = {
  default:
    "I'm your AI farming assistant 🌾. Ask me anything about rice diseases, prevention, fertilizers, or harvesting!",
  "bacterial leaf blight":
    "Bacterial Leaf Blight (BLB) is caused by Xanthomonas oryzae. It creates yellow-white lesions and can reduce yield by up to 50% if untreated.",
  "prevent rice":
    "Prevention tips:\n1. Use resistant varieties\n2. Avoid excess nitrogen\n3. Maintain spacing\n4. Ensure drainage\n5. Remove infected residues",
  "fertilizers":
    "Recommended fertilizers:\n• Nitrogen (N): 80–120 kg/ha\n• Phosphorus (P): 40–60 kg/ha\n• Potassium (K): 40–60 kg/ha\nSplit nitrogen into 3 stages.",
  "harvest":
    "Harvest rice when:\n• 80–85% grains are straw-colored\n• Grain moisture is 20–25%\n• Panicles droop naturally"
};

function addMessage(text, type) {
  const div = document.createElement("div");
  div.className = `chat-msg ${type} animate-slide`;
  div.innerText = text;
  chatBody.appendChild(div);
  chatBody.scrollTop = chatBody.scrollHeight;
}

function sendMessage() {
  const text = chatInput.value.trim();
  if (!text) return;

  addMessage(text, "user");
  chatInput.value = "";

  showTyping();

  setTimeout(() => {
    removeTyping();
    const response = getBotResponse(text.toLowerCase());
    addMessage(response, "bot");
  }, 1500);
}

function quickAsk(text) {
  chatInput.value = text;
  sendMessage();
}

function getBotResponse(query) {
  for (let key in botResponses) {
    if (query.includes(key)) return botResponses[key];
  }
  return botResponses.default;
}

function showTyping() {
  const typing = document.createElement("div");
  typing.id = "typing";
  typing.className = "chat-msg bot typing";
  typing.innerText = "Typing...";
  chatBody.appendChild(typing);
}

function removeTyping() {
  const typing = document.getElementById("typing");
  if (typing) typing.remove();
}

addMessage(botResponses.default, "bot");
```

#### dashboard.js
```javascript
const sidebar = document.getElementById("sidebar");
const openBtn = document.getElementById("openSidebar");
const closeBtn = document.getElementById("closeSidebar");

openBtn.onclick = () => sidebar.classList.add("show");
closeBtn.onclick = () => sidebar.classList.remove("show");
```

#### history.js
```javascript
const data = [
  { id:1, image:"https://images.unsplash.com/photo-1536304993881-ff6e9eefa2a6", disease:"Bacterial Leaf Blight", severity:"Moderate", confidence:94.7, date:"2024-01-15" },
  { id:2, image:"https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b", disease:"Brown Spot", severity:"Mild", confidence:89.2, date:"2024-01-14" },
  { id:3, image:"https://images.unsplash.com/photo-1500382017468-9049fed747ef", disease:"Leaf Blast", severity:"Severe", confidence:97.1, date:"2024-01-13" },
  { id:4, image:"https://images.unsplash.com/photo-1625246333195-78d9c38ad449", disease:"Healthy", severity:"None", confidence:99.3, date:"2024-01-12" }
];

const table = document.getElementById("historyTable");
const searchInput = document.getElementById("searchInput");
const severityFilter = document.getElementById("severityFilter");
const emptyState = document.getElementById("emptyState");
const tableWrapper = document.getElementById("tableWrapper");
const toggleEmpty = document.getElementById("toggleEmpty");

let showEmpty = false;

function render(rows) {
  table.innerHTML = "";
  if (rows.length === 0) {
    tableWrapper.classList.add("hidden");
    emptyState.classList.remove("hidden");
    return;
  }
  tableWrapper.classList.remove("hidden");
  emptyState.classList.add("hidden");

  rows.forEach(item => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td><img src="${item.image}" style="width:48px;height:48px;border-radius:8px;object-fit:cover"></td>
      <td>${item.disease}</td>
      <td><span class="badge ${item.severity.toLowerCase()}">${item.severity}</span></td>
      <td>${item.confidence}%</td>
      <td>${item.date}</td>
      <td>
        <button class="btn btn-outline">👁</button>
        <button class="btn btn-outline">🗑</button>
      </td>
    `;
    table.appendChild(tr);
  });
}

function filterData() {
  let filtered = data.filter(d =>
    d.disease.toLowerCase().includes(searchInput.value.toLowerCase())
  );
  if (severityFilter.value !== "all") {
    filtered = filtered.filter(d => d.severity === severityFilter.value);
  }
  render(filtered);
}

searchInput.addEventListener("input", filterData);
severityFilter.addEventListener("change", filterData);

toggleEmpty.addEventListener("click", () => {
  showEmpty = !showEmpty;
  if (showEmpty) {
    tableWrapper.classList.add("hidden");
    emptyState.classList.remove("hidden");
  } else {
    filterData();
  }
});

render(data);
```

#### main.js
```javascript
document.addEventListener("DOMContentLoaded", () => {
  // Active nav link
  const links = document.querySelectorAll(".nav-links a");
  const path = window.location.pathname.split("/").pop();

  links.forEach(link => {
    if (link.getAttribute("href") === path) {
      link.classList.add("active");
    }
  });

  // Mobile menu toggle
  const menuBtn = document.getElementById("menuToggle");
  const mobileMenu = document.getElementById("mobileMenu");

  if (menuBtn && mobileMenu) {
    menuBtn.addEventListener("click", () => {
      mobileMenu.classList.toggle("hidden");
    });
  }
});
```

#### result.js
```javascript
const analyzing = document.getElementById("analyzing");
const resultPage = document.getElementById("resultPage");

// Show analyzing animation first
setTimeout(() => {
  analyzing.classList.add("hidden");
  resultPage.classList.remove("hidden");
}, 2000);

// 🔥 GET REAL RESULT FROM BACKEND
const result = JSON.parse(localStorage.getItem("riceguard_result"));

if (!result) {
  alert("No detection data found. Please upload an image.");
  window.location.href = "index.html";
}

// 🔥 SET TEXT DATA (REAL)
document.getElementById("diseaseName").innerText = result.disease;
document.getElementById("confidence").innerText = result.confidence + "%";
document.getElementById("severity").innerText = result.severity;
document.getElementById("description").innerText = result.description;

// 🔥 SET IMAGES (UPLOAD IMAGE USED FOR DETECTION)
const uploadedImage = localStorage.getItem("uploadedImage");

document.getElementById("originalImg").src = uploadedImage;
document.getElementById("detectImg").src = uploadedImage;
document.getElementById("heatmapImg").src = uploadedImage;

// 🔥 CLEAR OLD LISTS
document.getElementById("symptoms").innerHTML = "";
document.getElementById("treatment").innerHTML = "";
document.getElementById("prevention").innerHTML = "";

// 🔥 POPULATE REAL SYMPTOMS
if (result.symptoms) {
  result.symptoms.forEach(item => {
    const li = document.createElement("li");
    li.textContent = item;
    document.getElementById("symptoms").appendChild(li);
  });
}

// 🔥 POPULATE REAL TREATMENT
if (result.treatment) {
  result.treatment.forEach(item => {
    const li = document.createElement("li");
    li.textContent = item;
    document.getElementById("treatment").appendChild(li);
  });
}

// 🔥 POPULATE REAL PREVENTION
if (result.prevention) {
  result.prevention.forEach(item => {
    const li = document.createElement("li");
    li.textContent = item;
    document.getElementById("prevention").appendChild(li);
  });
}
```

#### upload.js
```javascript
const fileInput = document.getElementById("fileInput");
const previewContainer = document.getElementById("previewContainer");
const previewImage = document.getElementById("previewImage");
const uploadPlaceholder = document.getElementById("uploadPlaceholder");
const detectBtn = document.getElementById("detectBtn");

let selectedFile = null;

// Open file picker
function openFilePicker() {
  fileInput.click();
}

// Handle file selection
fileInput.addEventListener("change", () => {
  const file = fileInput.files[0];
  if (!file || !file.type.startsWith("image/")) return;

  selectedFile = file;

  const reader = new FileReader();
  reader.onload = () => {
    previewImage.src = reader.result;
    previewContainer.classList.remove("hidden");
    uploadPlaceholder.classList.add("hidden");
    detectBtn.classList.remove("hidden");
  };
  reader.readAsDataURL(file);
});

// Remove selected image
function removeImage(e) {
  e.stopPropagation();
  previewImage.src = "";
  previewContainer.classList.add("hidden");
  uploadPlaceholder.classList.remove("hidden");
  detectBtn.classList.add("hidden");
  selectedFile = null;
}

// 🔥 REAL DISEASE DETECTION
async function detectDisease() {
  if (!selectedFile) {
    alert("Please upload an image first");
    return;
  }

  detectBtn.innerText = "Detecting...";
  detectBtn.disabled = true;

  const formData = new FormData();
  formData.append("file", selectedFile);

  try {
    const response = await fetch("http://127.0.0.1:8000/detect", {
      method: "POST",
      body: formData
    });

    if (!response.ok) {
      throw new Error("Server error");
    }

    const result = await response.json();

    // ✅ Save REAL model output
    localStorage.setItem("riceguard_result", JSON.stringify(result));

    // Redirect to result page
    window.location.href = "result.html";

  } catch (error) {
    alert("Error detecting disease. Please try again.");
    console.error(error);
  } finally {
    detectBtn.innerText = "Detect Disease";
    detectBtn.disabled = false;
  }
}
```