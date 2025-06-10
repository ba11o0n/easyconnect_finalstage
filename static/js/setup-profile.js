import { submitToBackend } from './api.js';

document.getElementById("profile-pic").addEventListener("change", function (e) {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = () => {
        const preview = document.getElementById("preview");
        preview.src = reader.result;
        preview.classList.remove("hidden");
      };
      reader.readAsDataURL(file);
    }
  });
  
  document.getElementById("profile-form").addEventListener("submit", (e) => {
    e.preventDefault();
    alert("Profile submitted! (you can connect backend later)");
  });
  