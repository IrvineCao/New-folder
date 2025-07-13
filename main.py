import streamlit as st
from utils.state import initialize_session_state
from utils.activity_logger import log_activity
import base64
import os

# Luôn khởi tạo state ở đầu
initialize_session_state()

# --- PHẦN XÁC THỰC NGƯỜI DÙNG Ở SIDEBAR ---
st.sidebar.markdown("---")
# Nếu người dùng đã đăng nhập, hiển thị thông tin và nút logout
if st.session_state.get('username'):
    st.sidebar.success(f"Logged in as: **{st.session_state.username}**")
    if st.sidebar.button("Logout"):
        log_activity(action="LOGOUT")
        st.session_state.username = None
        # Xóa các state khác để bắt đầu lại hoàn toàn
        for key in list(st.session_state.keys()):
            if key != 'dev_logs' and key != 'dev_mode_activated':
                del st.session_state[key]
        st.rerun()
# Nếu chưa, hiển thị form đăng nhập
else:
    st.sidebar.subheader("Login")
    name_input = st.sidebar.text_input("Please enter your name to begin", key="name_input")
    if st.sidebar.button("Start Session", key="login_button"):
        if name_input:
            st.session_state.username = name_input
            log_activity(action="LOGIN")
            st.rerun()
        else:
            st.sidebar.warning("Name cannot be empty.")

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
st.markdown("<h1 class='main-header'>Welcome to Data Exporter Pro</h1>", unsafe_allow_html=True)
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



# --- PHẦN DÀNH CHO NHÀ PHÁT TRIỂN ---
st.sidebar.markdown("---")
# Bạn có thể thay đổi mã bí mật này
SECRET_CODE = "irvine"

# Ô nhập mã bí mật
dev_code = st.sidebar.text_input("Developer Access", type="password", key="dev_access_code")

# Kích hoạt chế độ nhà phát triển nếu nhập đúng mã
if dev_code == SECRET_CODE:
    st.session_state.dev_mode_activated = True

# Hiển thị log nếu chế độ nhà phát triển đã được kích hoạt
if st.session_state.get('dev_mode_activated', False):
    st.sidebar.subheader("🛠️ Developer Log")

    # Hiển thị GIF
    gif_path = "giphy.gif"
    if os.path.exists(gif_path):
        try:
            with open(gif_path, "rb") as file_:
                contents = file_.read()
                data_url = base64.b64encode(contents).decode("utf-8")
            st.sidebar.markdown(
                f'<img src="data:image/gif;base64,{data_url}" alt="developer gif" style="border-radius: 10px; margin-bottom: 1em;">',
                unsafe_allow_html=True,
            )
        except Exception as e:
            st.sidebar.warning(f"Could not display GIF: {e}")
    
    # Nút để xóa log và tắt chế độ dev
    if st.sidebar.button("Clear Logs & Deactivate"):
        st.session_state.dev_logs = []
        st.session_state.dev_mode_activated = False
        st.rerun()
        
    # Hiển thị các log lỗi
    if not st.session_state.dev_logs:
        st.sidebar.info("No technical errors have been logged.")
    else:
        for log in st.session_state.dev_logs:
            with st.sidebar.expander(f"**{log['timestamp']} - {log['error_type']}**"):
                st.error(log['message'])
                st.code(log['traceback'], language='python')