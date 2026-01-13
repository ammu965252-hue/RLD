const analyzing = document.getElementById("analyzing");
const resultPage = document.getElementById("resultPage");

setTimeout(() => {
  analyzing.classList.add("hidden");
  resultPage.classList.remove("hidden");
}, 2000);

const image = localStorage.getItem("uploadedImage");

document.getElementById("originalImg").src = image;
document.getElementById("detectImg").src = image;
document.getElementById("heatmapImg").src = image;

const symptoms = [
  "Yellow-orange stripes on leaf blades",
  "Leaves wilt and roll up",
  "Creamy bacterial ooze",
  "V-shaped lesions from tips"
];

const treatment = [
  "Apply copper-based bactericides",
  "Use resistant rice varieties",
  "Avoid excess nitrogen",
  "Ensure drainage",
  "Remove infected debris"
];

const prevention = [
  "Use certified seeds",
  "Crop rotation",
  "Balanced fertilization",
  "Proper spacing"
];

symptoms.forEach(s => {
  const li = document.createElement("li");
  li.textContent = s;
  document.getElementById("symptoms").appendChild(li);
});

treatment.forEach((t, i) => {
  const li = document.createElement("li");
  li.textContent = t;
  document.getElementById("treatment").appendChild(li);
});

prevention.forEach(p => {
  const li = document.createElement("li");
  li.textContent = p;
  document.getElementById("prevention").appendChild(li);
});
