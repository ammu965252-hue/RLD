// PASSWORD TOGGLE
const togglePassword = document.getElementById("togglePassword");
const passwordInput = document.getElementById("password");

if (togglePassword) {
  togglePassword.onclick = () => {
    passwordInput.type =
      passwordInput.type === "password" ? "text" : "password";
  };
}

// LOGIN FORM
const loginForm = document.getElementById("loginForm");

if (loginForm) {
  loginForm.onsubmit = (e) => {
    e.preventDefault();

    const email = document.getElementById("email").value;
    const password = passwordInput.value;
    const remember = document.getElementById("remember").checked;

    console.log("LOGIN DATA:", { email, password, remember });

    alert("Login successful (frontend demo)");
    window.location.href = "dashboard.html";
  };
}
// ================= REGISTER LOGIC =================
const password = document.getElementById("password");
const confirmPassword = document.getElementById("confirmPassword");
const rules = {
  length: document.getElementById("rule-length"),
  upper: document.getElementById("rule-upper"),
  lower: document.getElementById("rule-lower"),
  number: document.getElementById("rule-number"),
};
const terms = document.getElementById("terms");
const registerBtn = document.getElementById("registerBtn");
const matchMsg = document.getElementById("matchMsg");

function updateRule(el, valid) {
  el.textContent = (valid ? "✔ " : "❌ ") + el.textContent.slice(2);
  el.style.color = valid ? "green" : "";
}

function validatePassword() {
  const val = password.value;

  const checks = {
    length: val.length >= 8,
    upper: /[A-Z]/.test(val),
    lower: /[a-z]/.test(val),
    number: /[0-9]/.test(val),
  };

  updateRule(rules.length, checks.length);
  updateRule(rules.upper, checks.upper);
  updateRule(rules.lower, checks.lower);
  updateRule(rules.number, checks.number);

  return Object.values(checks).every(Boolean);
}

function validateMatch() {
  const match = password.value === confirmPassword.value && confirmPassword.value !== "";
  matchMsg.classList.toggle("hidden", match);
  return match;
}

function toggleRegisterButton() {
  registerBtn.disabled = !(validatePassword() && validateMatch() && terms.checked);
}

password?.addEventListener("input", toggleRegisterButton);
confirmPassword?.addEventListener("input", toggleRegisterButton);
terms?.addEventListener("change", toggleRegisterButton);

// TOGGLE VISIBILITY
document.getElementById("toggleConfirm")?.addEventListener("click", () => {
  confirmPassword.type =
    confirmPassword.type === "password" ? "text" : "password";
});

// SUBMIT
document.getElementById("registerForm")?.addEventListener("submit", (e) => {
  e.preventDefault();
  alert("Account created successfully (frontend demo)");
  window.location.href = "login.html";
});
