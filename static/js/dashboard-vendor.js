// src/js/dashboard-vendor.js
import './main.js';

window.toggleSection = function (id) {
  const el = document.getElementById(id);
  el.style.display = el.style.display === 'none' ? 'block' : 'none';
};

window.toggleDescription = function (btn) {
  const card = btn.closest('.event-card');
  const desc = card.querySelector('.event-description');
  const vendors = card.querySelector('.vendor-list');

  if (desc.classList.contains('short')) {
    desc.textContent = "This event will bring together innovators in AI and emerging tech with keynote speakers, workshops, and networking opportunities. Vendors can showcase new products and gather attendee insights through Smartband interactions.";
    desc.classList.remove('short');
    vendors.style.display = 'block';
    btn.textContent = "Show Less";
  } else {
    desc.textContent = "A major showcase for AI innovations, smart devices, and data intelligence tools...";
    desc.classList.add('short');
    vendors.style.display = 'none';
    btn.textContent = "See More About This";
  }
};


window.downloadCSV = function () {
    const interactions = [
      { name: "Person 1", linkedin: "https://linkedin.com/in/person1", website: "" },
      { name: "Person 2", linkedin: "", website: "https://person2.dev" },
      { name: "Person 3", linkedin: "https://linkedin.com/in/person3", website: "https://person3.org" }
    ];
  
    const headers = ['Name', 'LinkedIn', 'Website'];
    const rows = interactions.map(person => [
      person.name,
      person.linkedin,
      person.website
    ]);
  
    let csvContent = "data:text/csv;charset=utf-8," 
      + headers.join(",") + "\n"
      + rows.map(e => e.join(",")).join("\n");
  
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "interactions.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };
  

  window.showPreview = function () {
    const email = document.querySelector('#vendor-register input[type="email"]').value;
    const linkedin = document.querySelector('#vendor-register input[placeholder*="LinkedIn"]').value;
    const website = document.querySelector('#vendor-register input[placeholder*="Website"]').value;
  
    document.getElementById("preview-email").textContent = email || "(not provided)";
    document.getElementById("preview-linkedin").textContent = linkedin || "(not provided)";
    document.getElementById("preview-website").textContent = website || "(not provided)";
  
    document.getElementById("modal-overlay").style.display = "block";
    document.getElementById("vendor-modal").style.display = "block";
  };
  
  window.hidePreview = function () {
    document.getElementById("modal-overlay").style.display = "none";
    document.getElementById("vendor-modal").style.display = "none";
  };
  
  window.submitVendor = function () {
    alert("Registration submitted!");
    hidePreview();
  };  