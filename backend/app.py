"""
Rice Leaf Disease Detection Web Application
A deep learning application for detecting diseases in rice leaves
"""

from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Rice Leaf Disease Detection API'})

if __name__ == '__main__':
    app.run(debug=True)
