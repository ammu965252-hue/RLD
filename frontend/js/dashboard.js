async function loadDashboard() {
  const res = await fetch("http://127.0.0.1:8000/history");
  const data = await res.json();

  // Total detections
  document.getElementById("totalDetections").innerText = data.length;

  // Unique diseases
  const diseaseSet = new Set(data.map(d => d.disease));
  document.getElementById("diseaseCount").innerText = diseaseSet.size;

  // Avg confidence
  if (data.length > 0) {
    const avg =
      data.reduce((sum, d) => sum + d.confidence, 0) / data.length;
    document.getElementById("avgConfidence").innerText =
      avg.toFixed(1) + "%";
  }

  // Severe cases
  const severe = data.filter(d => d.severity === "Severe").length;
  document.getElementById("severeCount").innerText = severe;

  // Disease distribution chart
  const diseaseCounts = {};
  data.forEach(d => {
    diseaseCounts[d.disease] = (diseaseCounts[d.disease] || 0) + 1;
  });

  const labels = Object.keys(diseaseCounts);
  const values = Object.values(diseaseCounts);

  const ctx = document.getElementById("distributionChart").getContext("2d");
  new Chart(ctx, {
    type: "pie",
    data: {
      labels: labels,
      datasets: [{
        data: values,
        backgroundColor: [
          "#FF6384",
          "#36A2EB",
          "#FFCE56",
          "#4BC0C0",
          "#9966FF",
          "#FF9F40"
        ]
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: "bottom"
        }
      }
    }
  });

  // Recent detections
  const recent = data.slice(0, 5);
  const recentList = document.getElementById("recentList");
  recentList.innerHTML = "";

  recent.forEach(d => {
    const div = document.createElement("div");
    div.className = "recent-item";
    div.innerHTML = `
      <span>${d.disease}</span>
      <small class="${d.severity.toLowerCase()}">${d.severity}</small>
    `;
    recentList.appendChild(div);
  });
}

loadDashboard();
