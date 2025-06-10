// src/js/dashboard-admin.js
import './main.js';

window.toggleNewEvent = function () {
  const form = document.getElementById('new-event-form');
  form.style.display = form.style.display === 'none' ? 'block' : 'none';
};
