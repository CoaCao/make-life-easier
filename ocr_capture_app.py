import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="OCR Client-side with Tesseract.js", layout="centered")

st.title("📸 OCR bằng Tesseract.js (chạy phía client)")

components.html("""
<!DOCTYPE html>
<html>
  <head>
    <script src="https://cdn.jsdelivr.net/npm/tesseract.js@4.0.2/dist/tesseract.min.js"></script>
    <style>
      video, canvas {
        width: 100%;
        max-width: 400px;
        margin-bottom: 10px;
      }
    </style>
  </head>
  <body>
    <video id="video" autoplay playsinline></video><br/>
    <button onclick="captureAndRecognize()">📸 Capture & OCR</button>
    <p><strong>Text:</strong></p>
    <textarea id="output" rows="6" style="width: 100%"></textarea>
    <canvas id="canvas" style="display: none;"></canvas>

    <script>
      const video = document.getElementById('video');
      const canvas = document.getElementById('canvas');
      const output = document.getElementById('output');

      // Yêu cầu quyền camera
      navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
          video.srcObject = stream;
        })
        .catch(err => {
          console.error("Không thể mở camera:", err);
          alert("Không thể mở camera. Hãy đảm bảo bạn đã cấp quyền.");
        });

      function captureAndRecognize() {
        const ctx = canvas.getContext('2d');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        Tesseract.recognize(canvas, 'eng', {
          logger: m => console.log(m)
        }).then(({ data: { text } }) => {
          output.value = text.trim();
        }).catch(err => {
          console.error("Lỗi OCR:", err);
          output.value = "Lỗi OCR!";
        });
      }
    </script>
  </body>
</html>
""", height=600)
