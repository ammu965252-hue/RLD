import requests
import os

# Test detect endpoint with an existing image
image_path = "uploads/healthy-62-.jpg"

if os.path.exists(image_path):
    with open(image_path, "rb") as f:
        files = {"file": ("healthy-62-.jpg", f, "image/jpeg")}
        response = requests.post("http://127.0.0.1:8000/detect", files=files)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
else:
    print(f"Image not found: {image_path}")
