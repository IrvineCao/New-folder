import streamlit as st

def display_user_message():
    """
    Checks and displays any message stored in session_state.
    The message is automatically cleared after display to prevent it from reappearing.
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
        
        # Clear the message after it has been displayed
        st.session_state.user_message = None

