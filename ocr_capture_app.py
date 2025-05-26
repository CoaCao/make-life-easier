import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="OCR Camera App", layout="centered")
st.title("📦 Expiry Date Scanner")

components.html("""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Expiry Date OCR</title>
  <style>
    video, canvas {
      width: 100%;
      max-width: 800px;
      border-radius: 8px;
    }

    #result {
      margin-top: 12px;
      font-size: 1.4rem;
      font-weight: bold;
      color: #003366;
      text-align: center;
      background: #f8f8f8;
      padding: 12px;
      border-radius: 8px;
    }

    button {
      margin-top: 10px;
      padding: 10px 20px;
      font-size: 1.1rem;
    }

    @media (max-width: 768px) {
      video, canvas {
        width: 100%;
        height: auto;
      }
    }
  </style>
</head>
<body>
  <h2 style="text-align:center;">📷 Scan Expiry Date</h2>
  <video id="video" autoplay muted playsinline></video>
  <canvas id="canvas" style="display:none;"></canvas>
  <div style="text-align:center;">
    <button onclick="captureAndRecognize()">🔍 Capture & Recognize</button>
  </div>
  <div id="result">OCR result will appear here...</div>

  <script src="https://cdn.jsdelivr.net/npm/tesseract.js@4/dist/tesseract.min.js"></script>
  <script>
    const video = document.getElementById("video");
    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");
    const resultBox = document.getElementById("result");

    // Rear camera if on mobile
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
        const binary = avg > 140 ? 255 : 0;
        data[i] = data[i + 1] = data[i + 2] = binary;
      }
      ctx.putImageData(imageData, 0, 0);
    }

    function extractExpiry(text) {
      const patterns = [
        /exp[\s:]*([0-9]{2}[\/\-.][0-9]{2,4})/i,
        /expiry[\s:]*([0-9]{2}[\/\-.][0-9]{2,4})/i,
        /use by[\s:]*([0-9]{2,4}[\/\-.][0-9]{1,2}(?:[\/\-.][0-9]{1,2})?)/i,
        /best before[\s:]*([0-9]{2,4}[\/\-.][0-9]{1,2}(?:[\/\-.][0-9]{1,2})?)/i,
        /\b([0-9]{4}[\/\-.][0-9]{2}[\/\-.][0-9]{2})\b/,    // e.g. 2025-09-05 or 2025.09.05
        /\b([0-9]{2}[\/\-.][0-9]{4})\b/,
        /\b([0-9]{2}[\/\-.][0-9]{2})\b/
      ];

      for (let pattern of patterns) {
        const match = text.match(pattern);
        if (match) return match[1];
      }
      return "";
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
        logger: m => console.log(m)
      }).then(({ data: { text } }) => {
        const cleaned = text.replace(/[^A-Za-z0-9 \/:\-\.]/g, '');
        const expiry = extractExpiry(cleaned);
        resultBox.textContent = expiry || "";
      }).catch(err => {
        console.error(err);
        resultBox.textContent = "";
      });
    }
  </script>
</body>
</html>
""", height=700)
