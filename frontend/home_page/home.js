function uploadCSV() {
  const fileInput = document.getElementById('csvFile');
  const file = fileInput.files[0];
  if (!file) {
    alert("Please select a CSV file.");
    return;
  }

  const formData = new FormData();
  formData.append('file', file);

  fetch('http://127.0.0.1:5000/upload', {
    method: 'POST',
    body: formData
  })
  .then(res => res.json())
  .then(data => {
    const output = document.getElementById('results');
    output.innerHTML = `
      <h2>Headers:</h2>
      <p>${data.headers.join(', ')}</p>
      <h2>Category:</h2>
      <p>${data.recommendations.category}</p>
      <h2>Recommended Pages:</h2>
      <ul>${data.recommendations.recommended_pages.map(p => `<li>${p}</li>`).join('')}</ul>
      <h2>Key Metrics:</h2>
      <ul>${data.recommendations.key_metrics.map(m => `<li>${m}</li>`).join('')}</ul>
      <h2>Filters:</h2>
      <ul>${data.recommendations.suggested_filters.map(f => `<li>${f}</li>`).join('')}</ul>
    `;
  })
  .catch(err => console.error(err));
}
