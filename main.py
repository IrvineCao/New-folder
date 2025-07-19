import streamlit as st
from utils.state import initialize_session_state

initialize_session_state()

# Page Configuration: Set the look and feel
st.set_page_config(
    page_title="Data Export | No More Waiting",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS: Enhance the Look ---
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css("assets/style.css")

# --- Main Content ---

# Header Section
st.markdown("<h1 class='main-title'>Data Export | No More Waiting</h1>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>The self-service data tool built out of pure necessity.</div>", unsafe_allow_html=True)

# The Irvine Story (you'll like this part)
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

# The 3-step process, redesigned for consistency
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

# Available Reports Section
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
        More export types will be available in the future. But Irvine is too lazy to do it.

        But Irvine will add them because he doesn't want to receive any more export requests.
    """)
    with st.expander("**Source?**", expanded=False):
        st.image("image.png")


st.write("") 

# Final Call to Action
st.success("You're in control now. 👉 Select a report from the menu on the left to get started.", icon="🎉")
