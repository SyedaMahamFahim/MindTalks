document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('uploadForm').addEventListener('submit', function (e) {
      e.preventDefault(); // Prevent page reload
      var formData = new FormData(this);
      var progressBar = document.getElementById('progressBar');
      var progressText = document.getElementById('progressText');
      progressBar.style.width = '0%'; // Initialize progress bar
      progressText.innerText = '0%'; // Initialize progress text
      document.getElementById('loading').style.display = 'block'; // Show loading spinner
      var xhr = new XMLHttpRequest();
      xhr.open('POST', '/upload', true);
      xhr.upload.onprogress = function (event) {
          if (event.lengthComputable) {
              var percentComplete = (event.loaded / event.total) * 100;
              progressBar.style.width = percentComplete + '%';
              progressText.innerText = percentComplete.toFixed(2) + '%';
          }
      };
      xhr.onload = function () {
          if (xhr.status === 200) {
              document.getElementById('loading').style.display = 'none'; // Hide loading spinner
              document.getElementById('success').style.display = 'block'; // Show success message
              // Display file path
              document.getElementById('filePath').innerText = xhr.responseText;
              setTimeout(function () {
                  document.getElementById('success').style.display = 'none'; // Hide success message after 3 seconds
              }, 3000);
          } else {
              document.getElementById('loading').style.display = 'none'; // Hide loading spinner
              document.getElementById('error').style.display = 'block'; // Show error message
              setTimeout(function () {
                  document.getElementById('error').style.display = 'none'; // Hide error message after 3 seconds
              }, 3000);
          }
      };
      xhr.send(formData);
  });
});
