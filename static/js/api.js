// src/js/api.js
export async function submitToBackend(endpoint, payload) {
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
  
    const result = await response.json();
    if (result.success) {
      alert("Success!");
    } else {
      alert("Error: " + result.message);
    }
  }
  