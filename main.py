import streamlit as st
from utils.state import initialize_session_state
import base64
import os

# Luôn khởi tạo state ở đầu
initialize_session_state()

# --- Phần nội dung chính của trang chủ (giữ nguyên) ---
st.set_page_config(
    page_title="Data Exporter Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            color: #2c3e50;
            text-align: center;
        }
        .sub-header {
            text-align: center;
            color: #6c757d;
        }
        .step-card {
            padding: 2em;
            border-radius: 10px;
            background: #252d34;
            text-align: center;
            height: 100%;
        }
        .step-icon {
            font-size: 3rem;
        }
    </style>
""", unsafe_allow_html=True)
st.markdown("<h1 class='main-header'>Welcome to Data Export Page</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Your Centralized Solution for Powerful Data Insights</p>", unsafe_allow_html=True)
st.divider()
st.subheader("Our Simple 3-Step Process")
col1, col2, col3 = st.columns(3, gap="large")
with col1:
    st.markdown("""
        <div class='step-card'>
            <div class='step-icon'>🖱️</div>
            <h4>1. Select & Filter</h4>
            <p>Choose a report from the sidebar and apply your desired filters like Workspace, Storefronts, and Date Range.</p>
        </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
        <div class='step-card'>
            <div class='step-icon'>📊</div>
            <h4>2. Preview & Analyze</h4>
            <p>Instantly get a preview of your data (the first 500 rows) along with a summary of the total dataset size.</p>
        </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
        <div class='step-card'>
            <div class='step-icon'>🚀</div>
            <h4>3. Export Full Data</h4>
            <p>With one click, export the complete dataset and download it as a clean, ready-to-use CSV file.</p>
        </div>
    """, unsafe_allow_html=True)

st.divider()
st.subheader("Available Data Exports")
with st.expander("📈 **Keyword Lab**", expanded=True):
    st.write("""
        Export comprehensive keyword data, including discovery metrics, estimated search volume, 
        and performance indicators like GMV, cost, clicks, and ROAS.
    """)
with st.expander("📈 **Digital Shelf Analytics**", expanded=True):
    st.write("""
        This suite contains multiple reports:
        - **Keyword Performance:** Analyze keyword effectiveness with metrics like e-score, benchmark CPC, and ad performance.
        - **Product Tracking:** Monitor product visibility and ranking for specific keywords.
    """)
st.info("👈 **Ready to start?** Select a report from the navigation menu on the left to begin your first export!", icon="🎉")