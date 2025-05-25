import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="OCR Camera App", layout="centered")

st.title("📷 OCR Camera - English & Japanese")

components.html("""
<!DOCTYPE html>
<html>
  <head>
    <script src="https://cdn.jsdelivr.net/npm/tesseract.js@4.0.2/dist/tesseract.min.js"></script>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
      body {
        font-family: sans-serif;
        text-align: center;
        margin: 0;
        padding: 0;
      }
      video {
        width: 100%;
        max-width: 400px;
        height: auto;
        aspect-ratio: 4 / 3;
        border: 2px solid #ccc;
        border-radius: 12px;
      }
      button {
        margin-top: 12px;
        padding: 10px 20px;
        font-size: 1rem;
        border-radius: 8px;
        background-color: #4CAF50;
        color: white;
        border: none;
      }
      textarea {
        width: 100%;
        max-width: 400px;
        height: 120px;
        margin-top: 14px;
        padding: 10px;
        font-size: 1rem;
        border-radius: 8px;
        border: 1px solid #999;
        resize: none;
      }
      canvas {
        display: none;
      }
    </style>
  </head>
  <body>
    <video id="video" autoplay playsinline></video><br/>
    <button onclick="captureAndRecognize()">📸 Capture & OCR</button>
    <textarea id="output" placeholder="Text will appear here..."></textarea>
    <canvas id="canvas"></canvas>

    <script>
      const video = document.getElementById('video');
      const canvas = document.getElementById('canvas');
      const output = document.getElementById('output');

      const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

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
          alert("🚫 Unable to access camera. Please check permissions.");
          console.error(err);
        });

      function captureAndRecognize() {
        const ctx = canvas.getContext('2d');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        Tesseract.recognize(canvas, 'eng+jpn', {
          logger: m => console.log(m)
        }).then(({ data: { text } }) => {
          output.value = text.trim();
        }).catch(err => {
          console.error("OCR error:", err);
          output.value = "❌ OCR error.";
        });
      }
    </script>
  </body>
</html>
""", height=680)
