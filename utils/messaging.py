import streamlit as st

def display_user_message():
    """
    Kiểm tra và hiển thị bất kỳ thông báo nào được lưu trong session_state.
    Thông báo sẽ tự động bị xóa sau khi hiển thị để không xuất hiện lại.
    """
    if st.session_state.get('user_message'):
        message = st.session_state.user_message
        msg_type = message.get("type", "info")
        msg_text = message.get("text", "")

        if msg_type == "error":
            st.error(msg_text, icon="🚨")
        elif msg_type == "warning":
            st.warning(msg_text, icon="⚠️")
        else:
            st.info(msg_text, icon="ℹ️")
        
        # Xóa thông báo sau khi đã hiển thị
        st.session_state.user_message = None

