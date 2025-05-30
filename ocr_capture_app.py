import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="📦 Make Life Easier !!!", layout="centered")
st.title("📦 Make Life Easier !!!")

components.html(open("index.html", encoding="utf8").read(), height=900)