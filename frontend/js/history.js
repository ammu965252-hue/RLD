const table = document.getElementById("historyTable");
const searchInput = document.getElementById("searchInput");
const severityFilter = document.getElementById("severityFilter");
const emptyState = document.getElementById("emptyState");
const tableWrapper = document.getElementById("tableWrapper");
const toggleEmpty = document.getElementById("toggleEmpty");

let allData = [];
let showEmpty = false;

// ================= FETCH REAL HISTORY =================
async function loadHistory() {
  try {
    const res = await fetch("http://127.0.0.1:8000/history");
    allData = await res.json();
    filterData();
  } catch (err) {
    console.error("Failed to load history", err);
    render([]);
  }
}

// ================= RENDER TABLE =================
function render(rows) {
  table.innerHTML = "";

  if (rows.length === 0) {
    tableWrapper.classList.add("hidden");
    emptyState.classList.remove("hidden");
    return;
  }

  tableWrapper.classList.remove("hidden");
  emptyState.classList.add("hidden");

  rows.forEach((item, index) => {
    const date = new Date(item.timestamp).toLocaleString();

    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>
        <img 
          src="http://127.0.0.1:8000${item.original_image}" 
          style="width:48px;height:48px;border-radius:8px;object-fit:cover"
        >
      </td>
      <td>${item.disease}</td>
      <td>
        <span class="badge ${item.severity.toLowerCase()}">
          ${item.severity}
        </span>
      </td>
      <td>${item.confidence}%</td>
      <td>${date}</td>
      <td style="text-align:right">
        <button class="btn btn-outline" onclick="viewResult(${index})">👁</button>
      </td>
    `;
    table.appendChild(tr);
  });
}

// ================= FILTER =================
function filterData() {
  let filtered = allData.filter(d =>
    d.disease.toLowerCase().includes(searchInput.value.toLowerCase())
  );

  if (severityFilter.value !== "all") {
    filtered = filtered.filter(d => d.severity === severityFilter.value);
  }

  render(filtered);
}

// ================= VIEW RESULT =================
function viewResult(index) {
  localStorage.setItem("riceguard_result", JSON.stringify(allData[index]));
  window.location.href = "result.html";
}

// ================= EVENTS =================
searchInput.addEventListener("input", filterData);
severityFilter.addEventListener("change", filterData);

toggleEmpty.addEventListener("click", () => {
  showEmpty = !showEmpty;
  if (showEmpty) {
    tableWrapper.classList.add("hidden");
    emptyState.classList.remove("hidden");
  } else {
    filterData();
  }
});

// ================= INIT =================
loadHistory();
