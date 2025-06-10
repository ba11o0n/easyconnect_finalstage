// src/js/dashboard-attendee.js
import './main.js';

window.toggleRegisterForm = function () {
  const form = document.getElementById('register-form');
  form.style.display = form.style.display === 'none' ? 'block' : 'none';
};

window.toggleDescription = function (btn) {
  const card = btn.closest('.event-card');
  const desc = card.querySelector('.event-description');
  const vendorList = card.querySelector('.vendor-list');

  if (desc.classList.contains('short')) {
    desc.textContent = "This event will bring together top minds in AI and emerging tech with dozens of booths and guest speakers throughout the day. Engage with booths, attend keynotes, and make real-time connections using your Smartband.";
    desc.classList.remove('short');
    vendorList.style.display = 'block';
    btn.textContent = "Show Less";
  } else {
    desc.textContent = "A full-day showcase of the latest in artificial intelligence and smart devices...";
    desc.classList.add('short');
    vendorList.style.display = 'none';
    btn.textContent = "See More About This";
  }
};
