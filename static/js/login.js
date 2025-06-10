import './main.js';

async function validateForm() {
  const email = document.querySelector('input[placeholder="Email Address"]')?.value.trim();
  const password = document.querySelector('input[placeholder="Password"]')?.value.trim();

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  if (!email || !emailRegex.test(email)) {
    alert("Please enter a valid email address.");
    return;
  }

  if (!password || password.length < 6) {
    alert("Password must be at least 6 characters.");
    return;
  }

  // Simulated backend response
  const result = { success: true, role: "admin" }; // replace this with real backend call

  if (result.success) {
    const role = result.role;
    if (role === 'admin') window.location.href = '/dashboard-admin.html';
    else if (role === 'vendor') window.location.href = '/dashboard-vendor.html';
    else window.location.href = '/dashboard-attendee.html';
  } else {
    alert("Login failed.");
  }

  // Later: call actual backend here
}

window.validateForm = validateForm;
