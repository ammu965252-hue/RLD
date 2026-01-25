const analyzing = document.getElementById("analyzing");
const resultPage = document.getElementById("resultPage");

setTimeout(() => {
  analyzing.classList.add("hidden");
  resultPage.classList.remove("hidden");
}, 1500);

const result = JSON.parse(localStorage.getItem("riceguard_result"));

if (!result) {
  alert("No detection data found");
  window.location.href = "index.html";
}

// TEXT
document.getElementById("diseaseName").innerText = result.disease;
document.getElementById("severity").innerText = result.severity;
document.getElementById("description").innerText = result.description;

// CONFIDENCE BAR
document.getElementById("confidenceBar").style.width =
  result.confidence + "%";

// LABEL
document.getElementById("detectionLabel").innerText =
  result.disease + " Detected";

// IMAGES
document.getElementById("originalImg").src =
  "http://127.0.0.1:8000" + result.original_image;

document.getElementById("detectImg").src =
  "http://127.0.0.1:8000" + result.result_image;

document.getElementById("heatmapImg").src =
  "http://127.0.0.1:8000" + result.result_image;

// CLEAR LISTS
["symptoms", "treatment", "prevention"].forEach(id => {
  document.getElementById(id).innerHTML = "";
});

// POPULATE
(result.symptoms || []).forEach(s =>
  document.getElementById("symptoms").innerHTML += `<li>${s}</li>`
);

(result.treatment || []).forEach(t =>
  document.getElementById("treatment").innerHTML += `<li>${t}</li>`
);

(result.prevention || []).forEach(p =>
  document.getElementById("prevention").innerHTML += `<li>${p}</li>`
);

// FEEDBACK SYSTEM
document.getElementById("feedbackForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const rating = document.querySelector('input[name="rating"]:checked')?.value;
  const comments = document.getElementById("comments").value;
  if (!rating) return alert("Please select a rating");

  await fetch("http://127.0.0.1:8000/feedback", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      detection_id: result.timestamp,
      rating: parseInt(rating),
      comments
    })
  });
  alert("Thank you for your feedback!");
});

// DOWNLOAD REPORT
document.getElementById("downloadReport").addEventListener("click", async () => {
  try {
    const response = await fetch("http://127.0.0.1:8000/generate_report", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(result)
    });
    const data = await response.json();
    const link = document.createElement("a");
    link.href = "http://127.0.0.1:8000" + data.file_url;
    link.download = "detection_report.pdf";
    link.click();
  } catch (error) {
    alert("Failed to generate report");
  }
});

// SHARE
document.getElementById("shareResult").addEventListener("click", () => {
  if (navigator.share) {
    navigator.share({
      title: "RiceGuard AI Detection Result",
      text: `Check out this disease detection result: ${result.disease}`,
      url: window.location.href
    });
  } else {
    navigator.clipboard.writeText(window.location.href);
    alert("Link copied to clipboard!");
  }
});

// DOWNLOAD REPORT
document.getElementById("downloadReport").addEventListener("click", async () => {
  try {
    const response = await fetch("http://127.0.0.1:8000/generate_report", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(result)
    });
    const data = await response.json();
    const link = document.createElement("a");
    link.href = "http://127.0.0.1:8000" + data.file_url;
    link.download = "detection_report.pdf";
    link.click();
  } catch (error) {
    alert("Failed to generate report");
  }
});

// SHARE
document.getElementById("shareResult").addEventListener("click", () => {
  if (navigator.share) {
    navigator.share({
      title: "RiceGuard AI Detection Result",
      text: `Check out this disease detection result: ${result.disease}`,
      url: window.location.href
    });
  } else {
    navigator.clipboard.writeText(window.location.href);
    alert("Link copied to clipboard!");
  }
});
