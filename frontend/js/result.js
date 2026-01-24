const analyzing = document.getElementById("analyzing");
const resultPage = document.getElementById("resultPage");

setTimeout(() => {
  analyzing.classList.add("hidden");
  resultPage.classList.remove("hidden");
}, 2000);

const result = JSON.parse(localStorage.getItem("riceguard_result"));

if (!result) {
  alert("No detection data found.");
  window.location.href = "index.html";
}

// 🔥 TEXT DATA
document.getElementById("diseaseName").innerText = result.disease;
document.getElementById("severity").innerText = result.severity;
document.getElementById("description").innerText = result.description;

// 🔥 CONFIDENCE BAR
document.getElementById("confidenceBar").style.width =
  result.confidence + "%";

// 🔥 LABEL
document.getElementById("detectionLabel").innerText =
  result.disease + " Detected";

// 🔥 IMAGES
document.getElementById("originalImg").src =
  "http://127.0.0.1:8000" + result.original_image;

document.getElementById("detectImg").src =
  "http://127.0.0.1:8000" + result.result_image;

// Heatmap (placeholder = detection image)
document.getElementById("heatmapImg").src =
  document.getElementById("detectImg").src;

// 🔥 CLEAR LISTS
["symptoms", "treatment", "prevention"].forEach(id => {
  document.getElementById(id).innerHTML = "";
});

// 🔥 POPULATE DATA
result.symptoms.forEach(item => {
  document.getElementById("symptoms").innerHTML += `<li>${item}</li>`;
});

result.treatment.forEach(item => {
  document.getElementById("treatment").innerHTML += `<li>${item}</li>`;
});

result.prevention.forEach(item => {
  document.getElementById("prevention").innerHTML += `<li>${item}</li>`;
});
