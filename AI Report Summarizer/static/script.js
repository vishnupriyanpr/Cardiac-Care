const fileInput = document.getElementById('fileInput');
const uploadForm = document.getElementById('uploadForm');
const statusText = document.getElementById('statusText');
const dropZone = document.getElementById('drop-zone');
const uploadIcon = document.querySelector('.upload-icon img');
const dropText = document.querySelectorAll('.drop-text');

fileInput.addEventListener('change', () => {
  if (fileInput.files.length > 0) {
    statusText.textContent = `Selected: ${fileInput.files[0].name}`;
  }
});

uploadForm.addEventListener('submit', () => {
  // Change cloud_upload.gif to loading.gif
  uploadIcon.src = "/static/loading.gif";
  uploadIcon.classList.add("loading-gif");

  // Update text during processing
  dropText.forEach(el => {
    el.textContent = "Extracting and summarizing your report...";
    el.style.color = '#00cfff';  // Sky blue theme color
    el.style.fontWeight = 'bold';
  });

  // Optional cleanup
  statusText.textContent = "";
});
