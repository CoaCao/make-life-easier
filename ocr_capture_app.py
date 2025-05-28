import streamlit as st
import streamlit.components.v1 as components
from db import init_db, add_product, get_products, update_product

init_db()
st.set_page_config(page_title="Product Expiry OCR", layout="centered")

tab1, tab2, tab3 = st.tabs(["📋 Product List", "➕ Add Product", "✏️ Edit Product"])

# Session for edited product
if "edit_product" not in st.session_state:
    st.session_state.edit_product = None

with tab1:
    st.subheader("📋 Product List")
    data = get_products()
    for row in data:
        id, name, created, exp = row
        col1, col2, col3, col4 = st.columns([4, 3, 3, 2])
        col1.write(name)
        col2.write(created)
        col3.write(exp)
        if col4.button("Edit", key=f"edit_{id}"):
            st.session_state.edit_product = row
            st.experimental_set_query_params(tab="Edit Product")

with tab2:
    st.subheader("➕ Add New Product")
    name = st.text_input("Product Name", key="name_input")
    if st.button("📷 Scan Name"):
        components.html(open("templates/ocr_camera.html", encoding="utf8").read(), height=600)

    exp_date = st.text_input("Expiration Date", key="exp_input")
    if st.button("📷 Scan Expiration Date"):
        components.html(open("templates/ocr_camera.html", encoding="utf8").read(), height=600)

    if st.button("Add Product"):
        if name and exp_date:
            add_product(name, exp_date)
            st.success("Product added successfully!")
        else:
            st.warning("Please fill in all fields.")

with tab3:
    if st.session_state.edit_product:
        st.subheader("✏️ Edit Product")
        id, name, created, exp = st.session_state.edit_product
        new_name = st.text_input("Product Name", value=name, key="edit_name")
        new_exp = st.text_input("Expiration Date", value=exp, key="edit_exp")

        if st.button("Save Changes"):
            update_product(id, new_name, new_exp)
            st.success("Product updated!")
            st.session_state.edit_product = None

# Lắng nghe dữ liệu từ iframe (client-side OCR)
st.markdown("""
<script>
window.addEventListener("message", (event) => {
    if (event.data?.type === "ocr-result") {
        const text = event.data.text;
        const nameInput = window.parent.document.querySelector('input[data-testid="stTextInput"][placeholder="Product Name"]');
        const expInput = window.parent.document.querySelector('input[data-testid="stTextInput"][placeholder="Expiration Date"]');
        if (nameInput && !nameInput.value) nameInput.value = text;
        if (expInput && !expInput.value) expInput.value = text;
    }
});
</script>
""", unsafe_allow_html=True)
