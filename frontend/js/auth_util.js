/**
 * RiceGuard AI - Authentication Utilities (Clean Version)
 */

(function () {
  "use strict";

  const STORAGE_KEY = "riceguard_user";

  function getStoredUser() {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      return stored ? JSON.parse(stored) : null;
    } catch (e) {
      console.error("Error parsing stored user:", e);
      return null;
    }
  }

  function getToken() {
    const user = getStoredUser();
    if (!user) {
      return null;
    }
    // Return JWT access token if available, otherwise fall back to user_id for legacy support
    return user.access_token || (user.user_id ? String(user.user_id) : null);
  }

  function getAuthHeaders() {
    const token = getToken();
    if (!token) return {};
    return {
      Authorization: `Bearer ${token}`,
    };
  }

  function isAuthenticated() {
    return !!getToken();
  }

  function requireAuthOrRedirect() {
    if (!isAuthenticated()) {
      localStorage.removeItem(STORAGE_KEY);
      window.location.href = "login.html";
      return false;
    }
    return true;
  }

  function setStoredUser(userObj) {
    if (!userObj || !userObj.user_id) {
      console.error("Invalid user object. user_id required.");
      return false;
    }
    localStorage.setItem(STORAGE_KEY, JSON.stringify(userObj));
    return true;
  }

  function clearSession() {
    localStorage.removeItem(STORAGE_KEY);
  }

  function logout() {
    clearSession();
    window.location.href = "login.html";
  }

  function handle401() {
    clearSession();
    window.location.href = "login.html";
  }

  // Expose globally
  window.getStoredUser = getStoredUser;
  window.getToken = getToken;
  window.getAuthHeaders = getAuthHeaders;
  window.isAuthenticated = isAuthenticated;
  window.requireAuthOrRedirect = requireAuthOrRedirect;
  window.setStoredUser = setStoredUser;
  window.clearSession = clearSession;
  window.logout = logout;
  window.handle401 = handle401;

  console.log("✓ Auth utilities loaded (Clean Version)");
})();
