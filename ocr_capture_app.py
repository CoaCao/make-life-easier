import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="OCR Camera App", layout="centered")
st.title("📷 OCR Camera - English")

components.html("""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Expiration Date Reader</title>
  <script src="https://cdn.jsdelivr.net/npm/tesseract.js@4.0.2/dist/tesseract.min.js"></script>
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <style>
    body {
      display: flex;
      flex-direction: column;
      align-items: center;
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 1rem;
      background-color: #f8f8f8;
    }

    h2 {
      margin-bottom: 10px;
    }

    video, canvas {
      width: 90vw;
      max-width: 320px;
      aspect-ratio: 4/3;
      border-radius: 8px;
      border: 2px solid #333;
      background: black;
    }

    button {
      margin-top: 12px;
      padding: 10px 20px;
      font-size: 1rem;
      border: none;
      border-radius: 6px;
      background-color: #007bff;
      color: white;
      cursor: pointer;
    }

    #result {
      margin-top: 14px;
      padding: 10px;
      background-color: #fff;
      width: 90vw;
      max-width: 320px;
      min-height: 60px;
      border-radius: 6px;
      text-align: center;
      box-shadow: 0 0 5px rgba(0,0,0,0.1);
    }
  </style>
</head>
<body>
  <h2>📦 Scan Expiration Date</h2>
  <video id="video" autoplay playsinline></video>
  <canvas id="canvas" style="display:none;"></canvas>
  <button onclick="captureAndRecognize()">📸 Capture</button>
  <div id="result">Waiting for capture...</div>

  <script>
    const video = document.getElementById("video");
    const canvas = document.getElementById("canvas");
    const resultBox = document.getElementById("result");

    // 🟢 Use rear camera if on mobile
    const constraints = {
      video: {
        facingMode: { ideal: "environment" }
      },
      audio: false
    };

    navigator.mediaDevices.getUserMedia(constraints)
      .then(stream => {
        video.srcObject = stream;
      })
      .catch(error => {
        console.error("Camera error:", error);
        resultBox.textContent = "⚠️ Failed to access camera.";
      });

    function captureAndRecognize() {
      const context = canvas.getContext("2d");
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      context.drawImage(video, 0, 0, canvas.width, canvas.height);

      resultBox.textContent = "🔍 Processing...";

      Tesseract.recognize(
        canvas,
        'eng+jpn', // English and Japanese support
        { logger: m => console.log(m) }
      ).then(({ data: { text } }) => {
        const expirationDate = extractExpirationDate(text);
        if (expirationDate) {
          const warning = checkDateStatus(expirationDate);
          resultBox.textContent = `📅 ${expirationDate} ${warning}`;
        } else {
          resultBox.textContent = "❌ No expiration date found.";
        }
      }).catch(err => {
        console.error(err);
        resultBox.textContent = "⚠️ OCR failed.";
      });
    }

    // 📅 Extract expiration-like date from text
    function extractExpirationDate(text) {
      const patterns = [
        /\b(20\d{2})[-\/\.](\d{1,2})[-\/\.](\d{1,2})\b/,  // YYYY-MM-DD
        /\b(\d{1,2})[-\/\.](\d{1,2})[-\/\.](20\d{2})\b/,  // DD/MM/YYYY or MM/DD/YYYY
        /\b(20\d{2})(\d{2})(\d{2})\b/                    // YYYYMMDD
      ];

      for (const pattern of patterns) {
        const match = text.match(pattern);
        if (match) {
          // Normalize date string
          const y = match[1].length === 4 ? match[1] : match[3];
          const m = ("0" + (match[2] || match[3])).slice(-2);
          const d = ("0" + (match[3] || match[2])).slice(-2);
          return `${y}-${m}-${d}`;
        }
      }

      return null;
    }

    // ⏳ Check if expired or near-expiry
    function checkDateStatus(dateStr) {
      const today = new Date();
      const expDate = new Date(dateStr);

      if (isNaN(expDate)) return "";

      const diff = Math.ceil((expDate - today) / (1000 * 60 * 60 * 24));
      if (diff < 0) {
        return "⚠️ Expired!";
      } else if (diff <= 7) {
        return `⚠️ Expiring in ${diff} day${diff === 1 ? "" : "s"}!`;
      } else {
        return "✅ Still valid";
      }
    }
  </script>
</body>
</html>


""", height=680)
