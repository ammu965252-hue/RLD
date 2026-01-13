document.addEventListener("DOMContentLoaded", () => {
  // Active nav link
  const links = document.querySelectorAll(".nav-links a");
  const path = window.location.pathname.split("/").pop();

  links.forEach(link => {
    if (link.getAttribute("href") === path) {
      link.classList.add("active");
    }
  });

  // Mobile menu toggle
  const menuBtn = document.getElementById("menuToggle");
  const mobileMenu = document.getElementById("mobileMenu");

  if (menuBtn && mobileMenu) {
    menuBtn.addEventListener("click", () => {
      mobileMenu.classList.toggle("hidden");
    });
  }
});
