import streamlit.components.v1 as components

def ocr_component():
    return components.html(open("camera_component_name.html", encoding="utf8").read(), height=500)


def index():
    return components.html(open("src/ocr_component/index.html", encoding="utf8").read(), height=1000)