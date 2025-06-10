import './main.js';
import { submitToBackend } from './api.js';

async function validateForm() {
  const name = document.querySelector('input[placeholder="Full Name"]')?.value.trim();
  const email = document.querySelector('input[placeholder="Email Address"]')?.value.trim();
  const password = document.querySelector('input[placeholder="Create Password"]')?.value.trim();
  const role = document.getElementById('user-role')?.value;

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  if (!name || name.length < 2) {
    alert("Please enter your full name.");
    return;
  }

  if (!email || !emailRegex.test(email)) {
    alert("Please enter a valid email address.");
    return;
  }

  if (!password || password.length < 6) {
    alert("Password must be at least 6 characters.");
    return;
  }

  if (!role) {
    alert("Please select your role.");
    return;
  }

  // Simulate backend response for demo
  const result = { success: true, role };

  if (result.success) {
    if (role === 'admin') window.location.href = '/dashboard-admin.html';
    else if (role === 'vendor') window.location.href = '/dashboard-vendor.html';
    else window.location.href = '/dashboard-attendee.html';
  } else {
    alert("Signup failed.");
  }

  // Later: submitToBackend('/api/signup', { name, email, password, role });
}

window.validateForm = validateForm;
