import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("products.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            expiration_date TEXT,
            created_date TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_product(name, expiration_date):
    conn = sqlite3.connect("products.db")
    c = conn.cursor()
    c.execute("INSERT INTO products (name, expiration_date, created_date) VALUES (?, ?, ?)",
              (name, expiration_date, datetime.now().strftime("%Y-%m-%d")))
    conn.commit()
    conn.close()

def get_products():
    conn = sqlite3.connect("products.db")
    c = conn.cursor()
    c.execute("SELECT id, name, created_date, expiration_date FROM products")
    rows = c.fetchall()
    conn.close()
    return rows

def update_product(id, name, expiration_date):
    conn = sqlite3.connect("products.db")
    c = conn.cursor()
    c.execute("UPDATE products SET name=?, expiration_date=? WHERE id=?",
              (name, expiration_date, id))
    conn.commit()
    conn.close()
