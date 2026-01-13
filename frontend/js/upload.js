const fileInput = document.getElementById("fileInput");
const previewContainer = document.getElementById("previewContainer");
const previewImage = document.getElementById("previewImage");
const uploadPlaceholder = document.getElementById("uploadPlaceholder");
const detectBtn = document.getElementById("detectBtn");

function openFilePicker() {
  fileInput.click();
}

fileInput.addEventListener("change", () => {
  const file = fileInput.files[0];
  if (!file || !file.type.startsWith("image/")) return;

  const reader = new FileReader();
  reader.onload = () => {
    previewImage.src = reader.result;
    previewContainer.classList.remove("hidden");
    uploadPlaceholder.classList.add("hidden");
    detectBtn.classList.remove("hidden");
    localStorage.setItem("uploadedImage", reader.result);
  };
  reader.readAsDataURL(file);
});

function removeImage(e) {
  e.stopPropagation();
  previewImage.src = "";
  previewContainer.classList.add("hidden");
  uploadPlaceholder.classList.remove("hidden");
  detectBtn.classList.add("hidden");
  localStorage.removeItem("uploadedImage");
}

function detectDisease() {
  window.location.href = "result.html";
}
