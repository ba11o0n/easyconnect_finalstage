window.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('scan-btn');
  const output = document.getElementById('scanner-output');
  const readerElem = document.getElementById('qr-reader');
  let scanner;

  function onScanSuccess(decodedText) {
    output.textContent = `Scanned Ticket ID: ${decodedText}`;
    
    scanner.stop().then(() => {
      readerElem.style.display = 'none';
      btn.disabled = false;
      
      function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
          const cookies = document.cookie.split(';');
          for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
            }
          }
        }
        return cookieValue;
      }
      
      fetch('/scan-ticket/', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ ticket_id: decodedText })
      })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          alert(`Assigned to Device: ${data.device_id}`);
        } else {
          alert(`Error: ${data.error}`);
        }
      })
      .catch(err => {
        console.error('Fetch error:', err);
        alert('Error contacting server');
      });
    });
  }

  btn?.addEventListener('click', () => {
    console.log('Scan button clicked');
    btn.disabled = true;
    readerElem.style.display = 'block';

    scanner = new Html5Qrcode('qr-reader');
    scanner.start(
      { facingMode: 'environment' },
      { fps: 10, qrbox: 250 },
      onScanSuccess
    ).catch(err => {
      console.error('Scanner start failed', err);
      output.textContent = 'Unable to start scanner';
      btn.disabled = false;
      readerElem.style.display = 'none';
    });
  });
});