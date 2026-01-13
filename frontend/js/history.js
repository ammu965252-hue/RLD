const data = [
  { id:1, image:"https://images.unsplash.com/photo-1536304993881-ff6e9eefa2a6", disease:"Bacterial Leaf Blight", severity:"Moderate", confidence:94.7, date:"2024-01-15" },
  { id:2, image:"https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b", disease:"Brown Spot", severity:"Mild", confidence:89.2, date:"2024-01-14" },
  { id:3, image:"https://images.unsplash.com/photo-1500382017468-9049fed747ef", disease:"Leaf Blast", severity:"Severe", confidence:97.1, date:"2024-01-13" },
  { id:4, image:"https://images.unsplash.com/photo-1625246333195-78d9c38ad449", disease:"Healthy", severity:"None", confidence:99.3, date:"2024-01-12" }
];

const table = document.getElementById("historyTable");
const searchInput = document.getElementById("searchInput");
const severityFilter = document.getElementById("severityFilter");
const emptyState = document.getElementById("emptyState");
const tableWrapper = document.getElementById("tableWrapper");
const toggleEmpty = document.getElementById("toggleEmpty");

let showEmpty = false;

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
      <td><img src="${item.image}" style="width:48px;height:48px;border-radius:8px;object-fit:cover"></td>
      <td>${item.disease}</td>
      <td><span class="badge ${item.severity.toLowerCase()}">${item.severity}</span></td>
      <td>${item.confidence}%</td>
      <td>${item.date}</td>
      <td>
        <button class="btn btn-outline">👁</button>
        <button class="btn btn-outline">🗑</button>
      </td>
    `;
    table.appendChild(tr);
  });
}

function filterData() {
  let filtered = data.filter(d =>
    d.disease.toLowerCase().includes(searchInput.value.toLowerCase())
  );
  if (severityFilter.value !== "all") {
    filtered = filtered.filter(d => d.severity === severityFilter.value);
  }
  render(filtered);
}

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

render(data);
