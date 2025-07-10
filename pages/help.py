import streamlit as st

st.title("Please Read")
try:
    # Giả định tệp help.md nằm ở thư mục gốc
    with open("help.md", "r", encoding="utf-8") as f:
        about = f.read()
    st.markdown(about)
except FileNotFoundError:
    st.error("File help.md not found.")