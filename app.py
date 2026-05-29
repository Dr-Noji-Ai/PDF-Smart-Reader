import streamlit as st
from pypdf import PdfReader
import sqlite3
from datetime import datetime

# =========================
# UI CONFIG
# =========================
st.set_page_config(page_title="Smart PDF Reader", layout="wide")
st.title("📄 Smart PDF Reader v1")

# =========================
# DATABASE
# =========================
conn = sqlite3.connect("pdf_app.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS bookmarks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT,
    page_number INTEGER,
    note TEXT,
    created_at TEXT
)
""")
conn.commit()

# =========================
# UPLOAD PDF
# =========================
file = st.file_uploader("📤 Upload PDF", type=["pdf"])

pdf_text = []
reader = None

if file:
    reader = PdfReader(file)

    for i, page in enumerate(reader.pages):
        try:
            text = page.extract_text()
        except:
            text = ""
        pdf_text.append(text)

    st.success(f"Loaded PDF with {len(pdf_text)} pages")

# =========================
# SEARCH
# =========================
search = st.text_input("🔍 Search in PDF")

# =========================
# DISPLAY PAGES
# =========================
if reader:
    for i, page_text in enumerate(pdf_text):

        if search:
            if search.lower() not in page_text.lower():
                continue

        st.markdown(f"### 📄 Page {i+1}")

        st.text(page_text[:2000])

        # =========================
        # BOOKMARK SYSTEM
        # =========================
        note = st.text_input(f"Add bookmark note (Page {i+1})", key=i)

        if st.button(f"💾 Save Bookmark {i+1}"):
            cursor.execute("""
                INSERT INTO bookmarks (filename, page_number, note, created_at)
                VALUES (?, ?, ?, ?)
            """, (
                file.name,
                i+1,
                note,
                datetime.now().isoformat()
            ))
            conn.commit()
            st.success("Bookmark saved")

# =========================
# VIEW BOOKMARKS
# =========================
st.markdown("## 🔖 Saved Bookmarks")

cursor.execute("SELECT filename, page_number, note, created_at FROM bookmarks ORDER BY id DESC")
rows = cursor.fetchall()

for r in rows:
    st.info(f"""
📁 {r[0]}  
📄 Page: {r[1]}  
📝 {r[2]}  
⏱ {r[3]}
""")
