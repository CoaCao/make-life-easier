import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="OCR Camera App", layout="centered")
st.title("📷 OCR Camera - English")

components.html("""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Client-side OCR</title>
  <style>
    video, canvas {
      width: 100%;
      max-width: 800px;
      border-radius: 8px;
    }

    #result {
      margin-top: 12px;
      font-size: 1.1rem;
      font-weight: bold;
      white-space: pre-wrap;
      background: #f0f0f0;
      padding: 12px;
      border-radius: 8px;
    }

    @media (max-width: 768px) {
      video, canvas {
        height: auto;
      }
    }
  </style>
</head>
<body>
  <h2>📷 OCR via Tesseract.js (English only)</h2>
  <video id="video" autoplay muted playsinline></video>
  <canvas id="canvas" style="display:none;"></canvas>
  <br />
  <button onclick="captureAndRecognize()">🔍 Capture & Recognize</button>
  <div id="result">OCR result will appear here...</div>

  <script src="https://cdn.jsdelivr.net/npm/tesseract.js@4/dist/tesseract.min.js"></script>
  <script>
    const video = document.getElementById("video");
    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");
    const resultBox = document.getElementById("result");

    // Open rear camera by default if on mobile
    const constraints = {
      audio: false,
      video: {
        facingMode: { ideal: "environment" },
        width: { ideal: 800 },
        height: { ideal: 600 }
      }
    };

    navigator.mediaDevices.getUserMedia(constraints)
      .then(stream => {
        video.srcObject = stream;
      })
      .catch(err => {
        console.error("Camera error:", err);
        alert("Cannot access camera.");
      });

    function preprocessImage(ctx, width, height) {
      const imageData = ctx.getImageData(0, 0, width, height);
      const data = imageData.data;
      for (let i = 0; i < data.length; i += 4) {
        const avg = (data[i] + data[i + 1] + data[i + 2]) / 3;
        const thresh = avg > 140 ? 255 : 0; // Binary threshold
        data[i] = data[i + 1] = data[i + 2] = thresh;
      }
      ctx.putImageData(imageData, 0, 0);
    }

    function captureAndRecognize() {
      const width = 800;
      const height = 600;
      canvas.width = width;
      canvas.height = height;

      ctx.drawImage(video, 0, 0, width, height);
      preprocessImage(ctx, width, height);

      resultBox.textContent = "⏳ Processing...";

      Tesseract.recognize(canvas, 'eng', {
        logger: m => console.log(m),
        tessedit_char_whitelist: 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,:;!?()[]{}-_=+'
      }).then(({ data: { text } }) => {
        resultBox.textContent = text || "No text found.";
      }).catch(err => {
        resultBox.textContent = "Error recognizing text.";
        console.error(err);
      });
    }
  </script>
</body>
</html>

""", height=680)
