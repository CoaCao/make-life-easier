import streamlit as st
from streamlit_webrtc import webrtc_streamer
import av
import cv2
import numpy as np
import easyocr

# Cấu hình page (phải là dòng đầu tiên)
st.set_page_config(page_title="OCR Camera App", layout="centered", page_icon="📷")

st.title("📷 OCR Camera App")

# Tạo OCR reader một lần
reader = easyocr.Reader(["en", "vi"], gpu=False)

# Dùng biến session_state để lưu frame hiện tại
if "current_frame" not in st.session_state:
    st.session_state.current_frame = None
if "ocr_text" not in st.session_state:
    st.session_state.ocr_text = ""


# Xử lý video frame
# Lưu frame vào processor (được thread-safe hơn)
class VideoProcessor:
    def __init__(self):
        self.latest_frame = None

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        self.latest_frame = img
        return av.VideoFrame.from_ndarray(img, format="bgr24")


# Cấu hình WebRTC
webrtc_ctx = webrtc_streamer(
    key="ocr-capture",
    video_processor_factory=VideoProcessor,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
)

# Nút Capture
if st.button("📸 Capture & OCR"):
    if webrtc_ctx.video_processor:
        frame = webrtc_ctx.video_processor.latest_frame
    else:
        frame = None

    if frame is not None:
        with st.spinner("🔍 Đang nhận diện văn bản..."):
            resized = cv2.resize(frame, (640, 480))
            results = reader.readtext(resized)
            extracted_text = "\n".join([res[1] for res in results])
            st.session_state.ocr_text = extracted_text
    else:
        st.warning("⚠️ Không lấy được hình ảnh từ camera. Hãy thử lại.")


# Hiển thị kết quả
st.text_area("📄 Kết quả trích xuất văn bản:", st.session_state.ocr_text, height=300)
