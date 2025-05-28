import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import datetime

DB = "products.db"

# Init DB
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        expiration_date TEXT,
        created_date TEXT
    )''')
    conn.commit()
    conn.close()

def add_product(name, expiration):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO products (name, expiration_date, created_date) VALUES (?, ?, ?)",
              (name, expiration, datetime.date.today().isoformat()))
    conn.commit()
    conn.close()

def update_product(pid, name, expiration):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("UPDATE products SET name=?, expiration_date=? WHERE id=?", (name, expiration, pid))
    conn.commit()
    conn.close()

def get_all_products():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT id, name, expiration_date, created_date FROM products ORDER BY created_date DESC")
    rows = c.fetchall()
    conn.close()
    return rows

st.set_page_config(page_title="Product OCR App", layout="centered")
st.title("📦 Product Manager with OCR")

init_db()

tab1, tab2, tab3 = st.tabs(["📋 Product List", "➕ Add Product", "✏️ Edit Product"])

# ===================== Tab 1: Product List ======================
with tab1:
    st.header("📋 Product List")
    products = get_all_products()
    if products:
        for p in products:
            col1, col2, col3, col4 = st.columns([3, 3, 3, 1])
            col1.write(p[1])
            col2.write(p[3])  # created_date
            col3.write(p[2])  # expiration_date
            if col4.button("✏️ Edit", key=f"edit_{p[0]}"):
                st.session_state["edit_id"] = p[0]
                # st.experimental_rerun()
    else:
        st.info("No products found.")

# ===================== Tab 2: Add Product ======================
with tab2:
    st.header("➕ Add Product")
    name = st.text_input("Name", key="name_input")
    if st.button("📷 Scan Name"):
        components.html(open("templates/camera_component_name.html").read(), height=500)

    expiration = st.text_input("Expiration Date", key="exp_input")
    if st.button("📷 Scan Expiration Date"):
        components.html(open("templates/camera_component_expiry.html").read(), height=500)

    if st.button("Add"):
        if name and expiration:
            add_product(name, expiration)
            st.success("✅ Product added!")
            # st.experimental_rerun()
        else:
            st.warning("Please fill all fields.")

# ===================== Tab 3: Edit Product ======================
with tab3:
    if "edit_id" in st.session_state:
        st.header("✏️ Edit Product")
        pid = st.session_state["edit_id"]
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("SELECT name, expiration_date FROM products WHERE id=?", (pid,))
        row = c.fetchone()
        conn.close()

        new_name = st.text_input("Name", value=row[0], key="edit_name")
        new_exp = st.text_input("Expiration Date", value=row[1], key="edit_exp")
        if st.button("Save"):
            update_product(pid, new_name, new_exp)
            st.success("✅ Product updated!")
            del st.session_state["edit_id"]
            # st.experimental_rerun()
    else:
        st.info("Select a product to edit from the list.")

# ===================== Receive result from iframe via JS ======================
components.html("""
<script>
  window.addEventListener("message", (event) => {
    const msg = event.data;
    console.log("msg: " + msg.text);
    if (msg?.type === "name_result") {
      const input = window.parent.document.querySelector('[id$="name_input"] input');
      if (input) {
        input.value = msg.text;
        input.dispatchEvent(new Event("input", { bubbles: true }));
      }
    } else if (msg?.type === "expiry_result") {
      const input = window.parent.document.querySelector('[id$="exp_input"] input');
      if (input) {
        input.value = msg.text;
        input.dispatchEvent(new Event("input", { bubbles: true }));
      }
    }
  });
</script>
""", height=0)
