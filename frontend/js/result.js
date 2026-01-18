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

// 🔥 SET TEXT DATA
document.getElementById("diseaseName").innerText = result.disease;
document.getElementById("confidence").innerText = result.confidence + "%";
document.getElementById("severity").innerText = result.severity;
document.getElementById("description").innerText = result.description;

// 🔥 SET IMAGES
// Original uploaded image
if (result.original_image) {
  document.getElementById("originalImg").src =
    "http://127.0.0.1:8000" + result.original_image;
}

// Detection image with YOLO bounding boxes
if (result.result_image) {
  document.getElementById("detectImg").src =
    "http://127.0.0.1:8000" + result.result_image;
}

// (Optional) heatmap placeholder
document.getElementById("heatmapImg").src =
  document.getElementById("detectImg").src;

// 🔥 CLEAR OLD LISTS
document.getElementById("symptoms").innerHTML = "";
document.getElementById("treatment").innerHTML = "";
document.getElementById("prevention").innerHTML = "";

// 🔥 POPULATE SYMPTOMS
if (result.symptoms && result.symptoms.length > 0) {
  result.symptoms.forEach(item => {
    const li = document.createElement("li");
    li.textContent = item;
    document.getElementById("symptoms").appendChild(li);
  });
}

// 🔥 POPULATE TREATMENT
if (result.treatment && result.treatment.length > 0) {
  result.treatment.forEach(item => {
    const li = document.createElement("li");
    li.textContent = item;
    document.getElementById("treatment").appendChild(li);
  });
}

// 🔥 POPULATE PREVENTION
if (result.prevention && result.prevention.length > 0) {
  result.prevention.forEach(item => {
    const li = document.createElement("li");
    li.textContent = item;
    document.getElementById("prevention").appendChild(li);
  });
}
