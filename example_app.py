import streamlit as st
from src.ocr_component.ocr_component import ocr_component

st.title("Demo OCR Component")

ocr_component()

name = st.text_input("Kết quả OCR sẽ điền vào đây")
st.write("Bạn nhập:", name)
