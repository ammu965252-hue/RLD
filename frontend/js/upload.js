const fileInput = document.getElementById("fileInput");
const previewContainer = document.getElementById("previewContainer");
const previewImage = document.getElementById("previewImage");
const uploadPlaceholder = document.getElementById("uploadPlaceholder");
const detectBtn = document.getElementById("detectBtn");

let selectedFile = null;

/* ================================
   OPEN FILE PICKER
================================ */
function openFilePicker() {
  fileInput.click();
}

/* ================================
   HANDLE FILE SELECTION
================================ */
fileInput.addEventListener("change", () => {
  const file = fileInput.files[0];

  if (!file) return;

  if (!file.type.startsWith("image/")) {
    alert("Please upload a valid image file");
    fileInput.value = "";
    return;
  }

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

/* ================================
   REMOVE IMAGE
================================ */
function removeImage(e) {
  e.stopPropagation();

  previewImage.src = "";
  previewContainer.classList.add("hidden");
  uploadPlaceholder.classList.remove("hidden");
  detectBtn.classList.add("hidden");

  fileInput.value = "";
  selectedFile = null;
}

/* ================================
   REAL DISEASE DETECTION
================================ */
async function detectDisease() {
  if (!selectedFile) {
    alert("Please upload an image first");
    return;
  }

  // Clear previous result
  localStorage.removeItem("riceguard_result");

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

    // Basic validation
    if (!result.disease) {
      throw new Error("Invalid response from model");
    }

    // Save result for result.html
    localStorage.setItem("riceguard_result", JSON.stringify(result));

    // Redirect
    window.location.href = "result.html";

  } catch (error) {
    console.error("Detection error:", error);
    alert("Detection failed. Please try another image.");
  } finally {
    detectBtn.innerText = "Detect Disease";
    detectBtn.disabled = false;
  }
}
