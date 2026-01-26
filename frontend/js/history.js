const table = document.getElementById("historyTable");
const searchInput = document.getElementById("searchInput");
const severityFilter = document.getElementById("severityFilter");
const emptyState = document.getElementById("emptyState");
const tableWrapper = document.getElementById("tableWrapper");
const toggleEmpty = document.getElementById("toggleEmpty");

let allData = [];
let showEmpty = false;

// ================= FETCH HISTORY =================
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

// ================= SAFE DATE =================
function formatDate(ts) {
  if (!ts) return "—";
  const d = new Date(ts);
  return isNaN(d.getTime()) ? "—" : d.toLocaleString();
}

// ================= RENDER =================
function render(rows) {
  table.innerHTML = "";

  if (rows.length === 0) {
    tableWrapper.classList.add("hidden");
    emptyState.classList.remove("hidden");
    return;
  }

  tableWrapper.classList.remove("hidden");
  emptyState.classList.add("hidden");

  rows.forEach(item => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>
        <img 
          src="http://127.0.0.1:8000${item.original_image || ''}" 
          width="48" height="48"
          onerror="this.src='data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDgiIGhlaWdodD0iNDgiIGZpbGw9IiNFRUVFRUUiLz48dGV4dCB4PSIyNCIgeT0iMjQiIGZpbGw9IiM5OTkiIHRleHQtYW5jaG9yPSJtaWRkbGUiPk5vIEltYWdlPC90ZXh0Pjwvc3ZnPg=='"
        />
      </td>
      <td>${item.disease}</td>
      <td><span class="badge ${item.severity.toLowerCase()}">${item.severity}</span></td>
      <td>${item.confidence}%</td>
      <td>${formatDate(item.timestamp)}</td>
      <td style="text-align:right">
        <button class="btn btn-outline" onclick='viewResult(${JSON.stringify(item)})'>👁</button>
        <button class="btn btn-danger" onclick="deleteDetection(${item.id})">🗑️</button>
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
function viewResult(item) {
  localStorage.setItem("riceguard_result", JSON.stringify(item));
  window.location.href = "result.html";
}

// ================= DELETE =================
async function deleteDetection(id) {
  if (!confirm("Delete this detection permanently?")) return;

  try {
    const res = await fetch(`http://127.0.0.1:8000/delete/${id}`, { method: "DELETE" });

    if (!res.ok) {
      alert("This detection no longer exists.");
      loadHistory();
      return;
    }

    alert("Detection deleted");
    loadHistory();
  } catch (err) {
    alert("Delete failed");
  }
}

// ================= EVENTS =================
searchInput.addEventListener("input", filterData);
severityFilter.addEventListener("change", filterData);

toggleEmpty.addEventListener("click", () => {
  showEmpty = !showEmpty;
  tableWrapper.classList.toggle("hidden", showEmpty);
  emptyState.classList.toggle("hidden", !showEmpty);
});

// ================= INIT =================
loadHistory();
