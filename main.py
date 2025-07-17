import streamlit as st
from utils.state import initialize_session_state

initialize_session_state()

# Cấu hình trang: Thiết lập giao diện và cảm xúc chung
st.set_page_config(
    page_title="Data Export | No More Waiting",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS tùy chỉnh: Nâng cấp giao diện ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');

        body {
            font-family: 'Inter', sans-serif;
            color: #e0e0e0; /* Thêm màu chữ mặc định cho dễ đọc hơn */
        }

        /* Hide the default Streamlit header and footer */
        .st-emotion-cache-18ni7ap, .st-emotion-cache-h4xjwg {
            display: none;
        }

        /* Title with a sick gradient */
        .main-title {
            font-size: 4.5rem;
            font-weight: 900;
            text-align: center;
            background: -webkit-linear-gradient(45deg, #ff007f, #00ffcc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            padding: 0.2em 0;
        }

        /* Sub-header for the ~vibes~ */
        .sub-header {
            text-align: center;
            font-size: 1.25rem;
            color: #a1a1aa; /* A softer gray */
            font-weight: 400;
            max-width: 600px;
            margin: 0 auto;
        }

        /* NEW: The "Irvine Rant" box */
        .rant-box {
            background-color: #1a1a1c;
            border-left: 4px solid #ff007f;
            padding: 1.5rem 2rem;
            margin: 2rem auto;
            border-radius: 8px;
            max-width: 800px;
        }

        .rant-box p {
            font-size: 1.05rem;
            color: #e0e0e0;
            line-height: 1.6;
        }

        .rant-box p strong {
            color: #ffffff;
        }

        /* The 3-step process cards */
        .step-card {
            background-color: #1c1c1e; /* Darker card */
            border: 1px solid #333;
            border-radius: 15px;
            padding: 2rem;
            text-align: center;
            height: 100%;
            transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
        }

        .step-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 30px rgba(255, 0, 127, 0.2); /* Pink glow on hover */
        }

        .step-icon {
            font-size: 4rem;
            line-height: 1;
        }

        .step-card h3 {
            font-weight: 700;
            color: #ffffff;
            margin-top: 1rem;
        }

        .step-card p {
            color: #a1a1aa;
            font-size: 0.95rem;
        }

        /* Styling for the expanders */
        .st-emotion-cache-p5msec {
            background-color: #1c1c1e;
            border-radius: 10px;
            border: 1px solid #333;
        }

        </style>
""", unsafe_allow_html=True)

# --- Nội dung chính ---

# Phần tiêu đề
st.markdown("<h1 class='main-title'>Data Export | No More Waiting</h1>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>The self-service data tool built out of pure necessity.</div>", unsafe_allow_html=True)

# Câu chuyện về Irvine (bạn thích phần này)
st.markdown("""
<div class='rant-box'>
    <p>
        Tired of having the perfect query, but nowhere to run it? <br>
        Tired of needing data but having to wait for <strong>Irvine</strong> to export it? <br>
        Let's be real, <strong>Irvine is tired of exporting data, too.</strong>
    </p>
    <p>
        So, he built this. A new export solution so you can stop waiting and start doing. Pull data directly from your laptop, PC, phone—whatever. This tool is fast, convenient, and the design is very human.
    </p>
    <p>
        All you do is fill in the fields, hit preview, and smash export. You get fresh, clean data with full columns and rows, perfectly formatted. No waiting, no begging, no knowing SQL.
    </p>
</div>
""", unsafe_allow_html=True)


st.divider()

# Quy trình 3 bước được làm lại cho nhất quán
st.subheader("Your New Workflow (The Irvine-Free Method)")
st.write("") 

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("""
        <div class='step-card'>
            <div class='step-icon'>🎯</div>
            <h3>1. Target Your Data</h3>
            <p>Instead of pinging Irvine, just pick a report from the sidebar and choose your own filters. You're the boss now.</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class='step-card'>
            <div class='step-icon'>🔍</div>
            <h3>2. Instant Preview</h3>
            <p>No more blind downloads. Get a quick look at the first 500 rows to make sure the data is looking 🔥 before you commit.</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class='step-card'>
            <div class='step-icon'>🚀</div>
            <h3>3. One-Click Export</h3>
            <p>Looks good? One click is all it takes. The full, clean, perfectly formatted CSV is yours in seconds. No wait time.</p>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# Phần các báo cáo có sẵn
st.subheader("What Can You Export?")

with st.expander("📈 **Keyword Lab**", expanded=True):
    st.write("""
        The full scoop on keywords. Get all discovery metrics, estimated search volume, performance data (GMV, cost, clicks), and more.
        Everything you used to ask Irvine for, now on demand.
    """)

with st.expander("💅 **Digital Shelf Analytics**", expanded=True):
    st.write("""
        A whole suite of reports to track your brand's presence.
        - **Keyword Performance**
        - **Product Tracking**
    """)

with st.expander("**Irvine's Promise**", expanded=True):
    st.write("""
        There will be more type of export in the future. But Irvine is too lazy to do it.

        But Irvine will make it because he dont want to recive any export request. 
    """)
    with st.expander("**Source?**", expanded=False):
        st.image("image.png")


st.write("") 

# Lời kêu gọi hành động cuối cùng
st.success("You're in control now. 👉 Select a report from the menu on the left to get started.", icon="🎉")
