import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration, WebRtcMode
import av
import easyocr


st.set_page_config(page_title="OCR Camera App", layout="centered", page_icon="🦈")

# Cấu hình WebRTC (dùng STUN server miễn phí của Google)
RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

# OCR Reader (chỉ khởi tạo 1 lần)
@st.cache_resource
def load_reader():
    return easyocr.Reader(["en", "ja"], gpu=False)

reader = load_reader()

# Xử lý khung hình video
class VideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.frame = None

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        self.frame = img
        return av.VideoFrame.from_ndarray(img, format="bgr24")


# Giao diện Streamlit
st.title("📷 Camera OCR - Trích xuất văn bản từ hình ảnh")

# Khởi tạo camera
ctx = webrtc_streamer(
    key="ocr-capture",
    mode=WebRtcMode.SENDRECV,
    rtc_configuration=RTC_CONFIGURATION,
    video_processor_factory=VideoProcessor,
    media_stream_constraints={
        "video": {"facingMode": "environment"},  # camera sau trên mobile
        "audio": False,
    },
    async_processing=True,
)

# Giao diện OCR
st.markdown("---")
if ctx.video_processor:
    if st.button("📸 Capture & OCR"):
        frame = ctx.video_processor.frame
        if frame is not None:
            with st.spinner("🔍 Đang nhận dạng văn bản..."):
                result = reader.readtext(frame)
                text = "\n".join([item[1] for item in result])
                st.success("✅ Nhận dạng hoàn tất!")
                st.text_area("📄 Văn bản trích xuất:", text, height=200)
        else:
            st.warning("❌ Không tìm thấy khung hình từ camera.")
else:
    st.info("📡 Đang khởi tạo camera... Vui lòng cấp quyền truy cập.")

