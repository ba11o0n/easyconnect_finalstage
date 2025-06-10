
document.addEventListener('DOMContentLoaded', () => {
  const scanBtn = document.getElementById('scan-btn');
  const output = document.getElementById('scanner-output');
  const readerElem = document.getElementById('qr-reader');
  let qrScanner;

  function handleScanSuccess(text) {
    output.textContent = `Scanned Ticket ID: ${text}`;
    qrScanner.stop().then(() => {
      fetch('/scan-ticket/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ticket_id: text })
      })
        .then(res => res.json())
        .then(data => {
          if (data.success) {
            alert(`Assigned to Device: ${data.device_id}`);
          } else {
            alert(data.error);
          }
        })
        .catch(() => alert('Error contacting server')); 
    });
  }

  scanBtn?.addEventListener('click', () => {
    scanBtn.disabled = true;
    readerElem.style.display = 'block';
    qrScanner = new Html5Qrcode('qr-reader');
    qrScanner.start({ facingMode: 'environment' }, { fps: 10, qrbox: 250 }, handleScanSuccess)
      .catch(err => {
        console.error(err);
        output.textContent = 'Unable to start scanner';
      });
  });
});

export async function joinEvent() {
  const code = document.getElementById('event-code').value;
  const res = await fetch('/join-employee-event/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ event_code: code })
  });
  const data = await res.json();
  alert(data.success ? `Joined event ID ${data.event_id}` : data.error);
}
