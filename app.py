import streamlit as st
from PyPDF2 import PdfReader
import sqlite3
from datetime import datetime

=========================================

PAGE CONFIG

=========================================

st.set_page_config(
page_title="Obad PDF Reader",
page_icon="📘",
layout="wide"
)

=========================================

PREMIUM UI

=========================================

st.markdown("""

<style>

/* اخفاء عناصر ستريملت */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* الخلفية */
.stApp{
    background:
    radial-gradient(circle at top left,#312e81,#0f172a 40%),
    linear-gradient(to bottom,#020617,#111827);
    color:white;
}

/* الحاوية */
.block-container{
    padding-top:2rem;
    max-width:1200px;
}

/* العنوان */
.main-title{
    text-align:center;
    font-size:52px;
    font-weight:800;
    color:white;
    margin-bottom:10px;
    text-shadow:0 0 20px rgba(99,102,241,.6);
}

/* الوصف */
.sub-title{
    text-align:center;
    color:#94a3b8;
    font-size:18px;
    margin-bottom:40px;
}

/* البطاقات */
.card{
    background:rgba(255,255,255,0.05);
    border:1px solid rgba(255,255,255,0.08);
    border-radius:24px;
    padding:24px;
    margin-bottom:20px;
    backdrop-filter: blur(14px);
    box-shadow:0 10px 40px rgba(0,0,0,0.35);
}

/* الأزرار */
.stButton > button{
    width:100%;
    border:none;
    border-radius:18px;
    padding:14px;
    font-size:16px;
    font-weight:700;
    color:white;

    background:
    linear-gradient(135deg,#4f46e5,#7c3aed,#06b6d4);

    box-shadow:
    0 8px 20px rgba(79,70,229,.45),
    inset 0 1px 1px rgba(255,255,255,.2);

    transition:0.25s;
}

.stButton > button:hover{
    transform:translateY(-2px) scale(1.02);
    box-shadow:
    0 14px 30px rgba(99,102,241,.6);
}

/* المدخلات */
.stTextInput input{
    background:#0f172a !important;
    color:white !important;
    border-radius:14px !important;
    border:1px solid #334155 !important;
}

textarea{
    background:#0f172a !important;
    color:white !important;
}

/* رفع الملفات */
[data-testid="stFileUploader"]{
    background:rgba(255,255,255,0.04);
    border-radius:20px;
    padding:20px;
    border:1px dashed #475569;
}

.search-box{
    margin-top:10px;
}

</style>""", unsafe_allow_html=True)

=========================================

HEADER

=========================================

st.markdown("""

<div class='main-title'>
📘 Obad PDF Reader
</div><div class='sub-title'>
3D Enterprise PDF Experience • Smart Search • Bookmarks
</div>
""", unsafe_allow_html=True)=========================================

DATABASE

=========================================

conn = sqlite3.connect("obad_pdf.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS bookmarks(
id INTEGER PRIMARY KEY AUTOINCREMENT,
filename TEXT,
page INTEGER,
note TEXT,
created_at TEXT
)
""")

conn.commit()

=========================================

LAYOUT

=========================================

left,right = st.columns([2,1])

=========================================

LEFT SIDE

=========================================

with left:

st.markdown("<div class='card'>", unsafe_allow_html=True)

uploaded = st.file_uploader(
    "📤 Upload PDF File",
    type=["pdf"]
)

search = st.text_input(
    "🔍 Search inside PDF",
    placeholder="Search any word..."
)

st.markdown("</div>", unsafe_allow_html=True)

=========================================

RIGHT SIDE

=========================================

with right:

st.markdown("<div class='card'>", unsafe_allow_html=True)

st.markdown("### 🔖 Saved Bookmarks")

cursor.execute("""
SELECT filename,page,note,created_at
FROM bookmarks
ORDER BY id DESC
LIMIT 10
""")

rows = cursor.fetchall()

if rows:
    for r in rows:
        st.info(f"""

📄 {r[0]}

📑 Page {r[1]}

📝 {r[2]}

⏱ {r[3]}
""")
else:
st.caption("No bookmarks yet")

st.markdown("</div>", unsafe_allow_html=True)

=========================================

PDF READER

=========================================

if uploaded:

st.markdown("<div class='card'>", unsafe_allow_html=True)

reader = PdfReader(uploaded)

st.success(f"✅ PDF Loaded Successfully ({len(reader.pages)} pages)")

for i,page in enumerate(reader.pages):

    try:
        text = page.extract_text()
    except:
        text = ""

    if search:
        if search.lower() not in text.lower():
            continue

    st.markdown(f"## 📄 Page {i+1}")

    st.text_area(
        f"content_{i}",
        value=text[:4000],
        height=250
    )

    note = st.text_input(
        f"Bookmark Note Page {i+1}",
        key=f"note_{i}"
    )

    if st.button(f"💾 Save Bookmark Page {i+1}"):

        cursor.execute("""
        INSERT INTO bookmarks(filename,page,note,created_at)
        VALUES(?,?,?,?)
        """,(
            uploaded.name,
            i+1,
            note,
            datetime.now().isoformat()
        ))

        conn.commit()

        st.success("Bookmark Saved")

st.markdown("</div>", unsafe_allow_html=True)

=========================================

FOOTER

=========================================

st.markdown("""

<div style='text-align:center;margin-top:40px;color:#64748b;font-size:14px;'>
Obad PDF Reader • Enterprise UI
</div>
""", unsafe_allow_html=True)
