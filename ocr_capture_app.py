import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="OCR Expiry Reader", layout="centered")
st.title("📦 Read Product Expiry Date")

components.html("""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Expiry OCR</title>
  <style>
    body {
      text-align: center;
      font-family: Arial, sans-serif;
    }

    video, canvas {
      width: 100%;
      max-width: 640px;
      height: auto;
      border-radius: 8px;
      margin: 0 auto;
      display: block;
    }

    #result {
      margin-top: 12px;
      font-size: 1.1rem;
      font-weight: bold;
      white-space: pre-wrap;
      background: #f0f0f0;
      padding: 12px;
      border-radius: 8px;
      max-width: 640px;
      margin-left: auto;
      margin-right: auto;
    }

    button {
      margin-top: 10px;
      padding: 10px 20px;
      font-size: 1rem;
      cursor: pointer;
    }

    @media (max-width: 768px) {
      video, canvas {
        height: 66.66vw; /* 2/3 chiều rộng trên điện thoại */
      }
    }
  </style>
</head>
<body>
  <h3>📷 Capture to Read Expiry Date</h3>
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

    const constraints = {
      audio: false,
      video: {
        facingMode: { ideal: "environment" },
        width: { ideal: 640 },
        height: { ideal: 480 }
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
        const thresh = avg > 140 ? 255 : 0;
        data[i] = data[i + 1] = data[i + 2] = thresh;
      }
      ctx.putImageData(imageData, 0, 0);
    }

    function extractExpiry(text) {
      const patterns = [
        /exp[\s:]*([0-9]{2}[\/\-][0-9]{2,4})/i,
        /expiry[\s:]*([0-9]{2}[\/\-][0-9]{2,4})/i,
        /use by[\s:]*([0-9]{2,4}[\/\-][0-9]{1,2}[\/\-]?[0-9]{0,2})/i,
        /([0-9]{2}[\/\-][0-9]{2}[\/\-][0-9]{2,4})/,
        /([0-9]{4}[\/\-][0-9]{1,2}[\/\-][0-9]{1,2})/
      ];

      for (let pattern of patterns) {
        const match = text.match(pattern);
        if (match) {
          return match[0];
        }
      }

      return null;
    }

    function captureAndRecognize() {
      const width = 640;
      const height = 480;
      canvas.width = width;
      canvas.height = height;

      ctx.drawImage(video, 0, 0, width, height);
      preprocessImage(ctx, width, height);

      resultBox.textContent = "⏳ Processing...";

      Tesseract.recognize(canvas, 'eng', {
        logger: m => console.log(m)
      }).then(({ data: { text } }) => {
        const cleaned = text.replace(/[^A-Za-z0-9 /\\:\\-]/g, '');
        const expiry = extractExpiry(cleaned);
        resultBox.textContent = expiry ? `✅ Found: ${expiry}` : "❌ No expiry date found.";
      }).catch(err => {
        resultBox.textContent = "Error recognizing text.";
        console.error(err);
      });
    }
  </script>
</body>
</html>
""", height=720)
