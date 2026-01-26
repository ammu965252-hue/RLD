const analyzing = document.getElementById("analyzing");
const resultPage = document.getElementById("resultPage");

// ================= SHOW RESULT PAGE =================
setTimeout(() => {
  analyzing.classList.add("hidden");
  resultPage.classList.remove("hidden");
}, 1200);

// ================= LOAD RESULT =================
const result = JSON.parse(localStorage.getItem("riceguard_result"));

if (!result || !result.disease) {
  alert("No detection data found");
  window.location.href = "index.html";
}

// ================= TEXT DATA =================
document.getElementById("diseaseName").innerText = result.disease;
document.getElementById("severity").innerText = result.severity || "—";
document.getElementById("description").innerText =
  result.description || "No description available";

// ================= CONFIDENCE =================
document.getElementById("confidenceBar").style.width =
  (result.confidence || 0) + "%";

// ================= LABEL =================
document.getElementById("detectionLabel").innerText =
  `${result.disease} Detected`;

// ================= IMAGES =================
const baseURL = "http://127.0.0.1:8000";

setImage("originalImg", result.original_image);
setImage("detectImg", result.result_image);
setImage("heatmapImg", result.result_image);

function setImage(id, path) {
  const img = document.getElementById(id);
  if (!path) {
    img.src = placeholderImage();
    return;
  }

  img.src = baseURL + path;
  img.onerror = () => {
    img.src = placeholderImage();
  };
}

function placeholderImage() {
  return "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgZmlsbD0iI0U1RTVFNSI+PHRleHQgeD0iMTAwIiB5PSIxMDAiIGZvbnQtc2l6ZT0iMTQiIGZpbGw9IiM5OTkiIHRleHQtYW5jaG9yPSJtaWRkbGUiPk5vIEltYWdlPC90ZXh0Pjwvc3ZnPg==";
}

// ================= CLEAR LISTS =================
["symptoms", "treatment", "prevention"].forEach(id => {
  document.getElementById(id).innerHTML = "";
});

// ================= POPULATE LISTS =================
(result.symptoms || []).forEach(s =>
  document.getElementById("symptoms").innerHTML += `<li>${s}</li>`
);

(result.treatment || []).forEach(t =>
  document.getElementById("treatment").innerHTML += `<li>${t}</li>`
);

(result.prevention || []).forEach(p =>
  document.getElementById("prevention").innerHTML += `<li>${p}</li>`
);

// ================= FEEDBACK =================
document.getElementById("feedbackForm").addEventListener("submit", async e => {
  e.preventDefault();

  const rating = document.querySelector('input[name="rating"]:checked')?.value;
  const comments = document.getElementById("comments").value;

  if (!rating) {
    alert("Please select a rating");
    return;
  }

  if (!result.detection_id) {
    alert("Cannot submit feedback: missing detection ID");
    return;
  }

  try {
    const res = await fetch(`${baseURL}/feedback`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        detection_id: result.detection_id,
        rating: parseInt(rating),
        comments
      })
    });

    if (!res.ok) throw new Error("Feedback failed");

    alert("Thank you for your feedback!");
    document.getElementById("feedbackForm").reset();
  } catch (err) {
    console.error(err);
    alert("Failed to submit feedback");
  }
});

// ================= DOWNLOAD REPORT =================
document.getElementById("downloadReport").addEventListener("click", async () => {
  try {
    const res = await fetch(`${baseURL}/generate_report`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(result)
    });

    if (!res.ok) throw new Error();

    const data = await res.json();
    const link = document.createElement("a");
    link.href = baseURL + data.file_url;
    link.download = "riceguard_report.pdf";
    link.click();
  } catch {
    alert("Failed to generate report");
  }
});

// ================= SHARE =================
document.getElementById("shareResult").addEventListener("click", () => {
  if (navigator.share) {
    navigator.share({
      title: "RiceGuard AI Detection Result",
      text: `Disease detected: ${result.disease}`,
      url: window.location.href
    });
  } else {
    navigator.clipboard.writeText(window.location.href);
    alert("Link copied to clipboard!");
  }
});
