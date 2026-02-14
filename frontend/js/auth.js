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
  loginForm.onsubmit = async (e) => {
    e.preventDefault();

    const email = document.getElementById("email").value;
    const password = passwordInput.value;

    try {
      const response = await fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (response.ok) {
        // Store user object in localStorage
        const user = {
          user_id: data.user_id,
          full_name: data.full_name,
          email: data.email,
        };
        localStorage.setItem("riceguard_user", JSON.stringify(user));
        
        console.log("✅ Login successful:", user);
        window.location.href = "home.html";
      } else {
        // Show error alert with backend message
        alert(data.error || data.detail || "Login failed. Please try again.");
      }
    } catch (error) {
      console.error("Login error:", error);
      alert("Login error: " + error.message);
    }
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
document.getElementById("registerForm")?.addEventListener("submit", async (e) => {
  e.preventDefault();
  
  const fullName = document.getElementById("fullName").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  try {
    const response = await fetch("http://127.0.0.1:8000/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ full_name: fullName, email, password }),
    });

    const data = await response.json();

    if (response.ok) {
      console.log("✅ Registration successful:", data);
      alert("Account created successfully! Redirecting to login...");
      window.location.href = "login.html";
    } else {
      // Show alert with backend error message
      alert(data.error || "Registration failed. Please try again.");
    }
  } catch (error) {
    console.error("Registration error:", error);
    alert("Registration error: " + error.message);
  }
});
