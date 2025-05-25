import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="OCR Client-side", layout="centered")

st.title("📷 OCR bằng Tesseract.js (Client-side, camera sau)")

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
        border: 1px solid #ccc;
        border-radius: 8px;
      }
    </style>
  </head>
  <body>
    <video id="video" autoplay playsinline></video><br/>
    <button onclick="captureAndRecognize()">📸 Chụp & OCR</button>
    <p><strong>Kết quả OCR:</strong></p>
    <textarea id="output" rows="6" style="width: 100%"></textarea>
    <canvas id="canvas" style="display: none;"></canvas>

    <script>
      const video = document.getElementById('video');
      const canvas = document.getElementById('canvas');
      const output = document.getElementById('output');

      // Phát hiện thiết bị di động
      const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

      // Chọn facingMode = 'environment' nếu trên mobile
      const constraints = {
        video: {
          facingMode: isMobile ? { exact: "environment" } : "user"
        }
      };

      navigator.mediaDevices.getUserMedia(constraints)
        .then(stream => {
          video.srcObject = stream;
        })
        .catch(err => {
          console.error("Không thể mở camera:", err);
          alert("Không thể mở camera. Vui lòng cấp quyền truy cập camera và thử lại.");
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
          output.value = "Lỗi khi nhận dạng văn bản!";
        });
      }
    </script>
  </body>
</html>
""", height=620)
