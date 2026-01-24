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

  // 🔥 CLEAR OLD RESULT
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

    const result = await response.json();

    // 🔥 SAVE NEW RESULT
    localStorage.setItem("riceguard_result", JSON.stringify(result));

    window.location.href = "result.html";

  } catch (error) {
    alert("Detection failed. Try again.");
    console.error(error);
  } finally {
    detectBtn.innerText = "Detect Disease";
    detectBtn.disabled = false;
  }
}
