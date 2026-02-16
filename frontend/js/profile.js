/* ===========================
   FETCH USER PROFILE
   ============================ */
async function fetchUserProfile() {
  // Check authentication
  if (!window.requireAuthOrRedirect || !window.requireAuthOrRedirect()) {
    return; // Redirects to login if not authenticated
  }

  try {
    // Get auth headers from centralized helper
    const headers = window.getAuthHeaders ? window.getAuthHeaders() : {};
    const response = await fetch("http://127.0.0.1:8000/me", { method: "GET", headers });

    const data = await response.json();
    if (!response.ok) {
      const msg = data?.detail || data?.error || `Failed to fetch profile: ${response.status}`;
      if (response.status === 401) {
        if (window.handle401) {
          window.handle401();
        } else {
          localStorage.removeItem('riceguard_user');
          window.location.href = 'login.html';
        }
        return;
      }
      throw new Error(msg);
    }
    // Populate form fields
    document.getElementById("email").value = data.email || "";
    document.getElementById("name").value = data.name || "";
    document.getElementById("nickname").value = data.nickname || "";
  } catch (error) {
    console.error("Fetch profile error:", error);
    alert("Could not load profile. " + error.message);
  }
}

/* ===========================
   SAVE PROFILE
   ============================ */
document.getElementById("saveProfile")?.addEventListener("click", async () => {
  // Check authentication
  if (!window.requireAuthOrRedirect || !window.requireAuthOrRedirect()) {
    return; // Redirects to login if not authenticated
  }

  const email = document.getElementById("email").value.trim();
  const name = document.getElementById("name").value.trim();
  const nickname = document.getElementById("nickname").value.trim();

  if (!email) {
    alert("Email is required.");
    return;
  }

  try {
    // Get auth headers from centralized helper
    const headers = window.getAuthHeaders ? window.getAuthHeaders() : {};
    headers['Content-Type'] = 'application/json';

    const response = await fetch("http://127.0.0.1:8000/update-profile", {
      method: "PUT",
      headers,
      body: JSON.stringify({ email: email || null, name: name || null, nickname: nickname || null }),
    });

    const data = await response.json();

    if (response.ok) {
      alert("Profile updated successfully!");
      // Update localStorage with new user data
      const stored = (window.getStoredUser && window.getStoredUser()) || {};
      stored.email = data.user?.email || stored.email;
      if (window.setStoredUser && typeof window.setStoredUser === 'function') {
        window.setStoredUser(stored);
      } else {
        localStorage.setItem('riceguard_user', JSON.stringify(stored));
      }
    } else {
      alert("Error: " + (data.detail || data.message || "Failed to update profile"));
      if (response.status === 401) {
        if (window.handle401) {
          window.handle401();
        } else {
          localStorage.removeItem('riceguard_user');
          window.location.href = 'login.html';
        }
      }
    }
  } catch (error) {
    console.error("Save profile error:", error);
    alert("Error updating profile: " + error.message);
  }
});

/* ===========================
   CHANGE PASSWORD
   ============================ */
document.getElementById("changePasswordBtn")?.addEventListener("click", async () => {
  // Check authentication
  if (!window.requireAuthOrRedirect || !window.requireAuthOrRedirect()) {
    return; // Redirects to login if not authenticated
  }

  const oldPassword = document.getElementById("oldPassword").value;
  const newPassword = document.getElementById("newPassword").value;

  if (!oldPassword || !newPassword) {
    alert("Both old and new passwords are required.");
    return;
  }

  if (oldPassword === newPassword) {
    alert("New password must be different from old password.");
    return;
  }

  try {
    const headers = (window.getAuthHeaders && window.getAuthHeaders()) || {};
    headers['Content-Type'] = 'application/json';

    const response = await fetch("http://127.0.0.1:8000/change-password", {
      method: "PUT",
      headers,
      body: JSON.stringify({ old_password: oldPassword, new_password: newPassword }),
    });

    const data = await response.json();

    if (response.ok) {
      alert("Password changed successfully!");
      document.getElementById("oldPassword").value = "";
      document.getElementById("newPassword").value = "";
    } else {
      alert("Error: " + (data.detail || data.message || "Failed to change password"));
      if (response.status === 401) {
        if (window.handle401) {
          window.handle401();
        } else {
          localStorage.removeItem('riceguard_user');
          window.location.href='login.html';
        }
      }
    }
  } catch (error) {
    console.error("Change password error:", error);
    alert("Error changing password: " + error.message);
  }
});

/* ===========================
   SIDEBAR TOGGLE
   ============================ */
document.getElementById("openSidebar")?.addEventListener("click", () => {
  document.getElementById("sidebar").classList.add("active");
});

document.getElementById("closeSidebar")?.addEventListener("click", () => {
  document.getElementById("sidebar").classList.remove("active");
});

/* ===========================
   INIT
   ============================ */
document.addEventListener("DOMContentLoaded", () => {
  fetchUserProfile();
});
