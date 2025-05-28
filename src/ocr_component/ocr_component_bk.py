import streamlit.components.v1 as components

def ocr_component():
    return components.html("""
    <html>
    <body>
      <video id="video" width="320" height="240" autoplay></video><br>
      <button id="capture">Capture</button>
      <canvas id="canvas" width="320" height="240" style="display: none;"></canvas>
      <script src="https://cdn.jsdelivr.net/npm/tesseract.js@4.0.2/dist/tesseract.min.js"></script>
      <script>
        const video = document.getElementById('video');
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        const captureBtn = document.getElementById('capture');

        navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
          video.srcObject = stream;
        });

        captureBtn.onclick = async () => {
          ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
          const dataUrl = canvas.toDataURL('image/png');

          const result = await Tesseract.recognize(dataUrl, 'eng');
          const text = result.data.text;

          const streamlitDoc = window.parent.document;
          const streamlitInput = streamlitDoc.querySelector('input[data-testid="stTextInput"]');
          if (streamlitInput) {
            streamlitInput.value = text;
            streamlitInput.dispatchEvent(new Event('input', { bubbles: true }));
          }
        };
      </script>
    </body>
    </html>
    """, height=300)
