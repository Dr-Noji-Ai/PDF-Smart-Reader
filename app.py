import streamlit as st
from pypdf import PdfReader
import io

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Obad PDF Reader",
    page_icon="📘",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

body {
    background-color: #0e1117;
    color: white;
}

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    color: #4fc3f7;
    margin-bottom: 20px;
}

.card {
    background: linear-gradient(
        145deg,
        rgba(255,255,255,0.08),
        rgba(255,255,255,0.03)
    );

    border-radius: 20px;
    padding: 20px;
    margin-bottom: 20px;

    border: 1px solid rgba(255,255,255,0.08);

    box-shadow:
        0 8px 32px rgba(0,0,0,0.35),
        inset 0 1px 1px rgba(255,255,255,0.08);
}

.stButton > button {

    width: 100%;
    border-radius: 18px;
    height: 55px;

    border: none;

    background: linear-gradient(
        145deg,
        #4fc3f7,
        #1976d2
    );

    color: white;
    font-size: 18px;
    font-weight: bold;

    box-shadow:
        0 6px 20px rgba(0,0,0,0.35);

    transition: 0.3s;
}

.stButton > button:hover {
    transform: scale(1.02);
}

.search-box {
    background: rgba(255,255,255,0.05);
    padding: 15px;
    border-radius: 15px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# TITLE
# =====================================================

st.markdown(
    "<div class='main-title'>📘 Obad PDF Reader</div>",
    unsafe_allow_html=True
)

# =====================================================
# SESSION
# =====================================================

if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = []

# =====================================================
# FILE UPLOAD
# =====================================================

uploaded_pdf = st.file_uploader(
    "📤 Upload PDF",
    type=["pdf"]
)

# =====================================================
# MAIN
# =====================================================

if uploaded_pdf:

    pdf = PdfReader(uploaded_pdf)

    full_text = ""

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("📄 PDF Information")

    st.write(f"Pages: {len(pdf.pages)}")

    for page in pdf.pages:

        try:
            text = page.extract_text()

            if text:
                full_text += text + "\n"

        except:
            pass

    st.success("✅ PDF Loaded Successfully")

    st.markdown("</div>", unsafe_allow_html=True)

    # =====================================================
    # SEARCH
    # =====================================================

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("🔍 Search Inside PDF")

    search = st.text_input("Enter word or sentence")

    if search:

        if search.lower() in full_text.lower():

            st.success("✅ Text Found")

            index = full_text.lower().find(search.lower())

            start = max(0, index - 300)
            end = min(len(full_text), index + 300)

            st.text_area(
                "Result",
                full_text[start:end],
                height=250
            )

        else:
            st.error("❌ Not Found")

    st.markdown("</div>", unsafe_allow_html=True)

    # =====================================================
    # BOOKMARKS
    # =====================================================

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("🔖 Bookmarks")

    bookmark = st.text_input("Add Bookmark")

    if st.button("➕ Save Bookmark"):

        if bookmark.strip():
            st.session_state.bookmarks.append(bookmark)

    for b in st.session_state.bookmarks:
        st.write("📌", b)

    st.markdown("</div>", unsafe_allow_html=True)

    # =====================================================
    # FULL TEXT
    # =====================================================

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("📖 PDF Text")

    st.text_area(
        "Content",
        full_text,
        height=400
    )

    st.markdown("</div>", unsafe_allow_html=True)
