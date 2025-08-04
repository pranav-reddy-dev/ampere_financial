import streamlit as st
from sidebar import sidebar_ui
from chat_interface import chat_ui

st.set_page_config(
    page_title="Ampere Copilot",
    page_icon="app/weblogo.png",
    layout="wide",
    initial_sidebar_state="auto"
)

st.markdown("""
    <style>
        .centered-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 80vh;
        }
    </style>
""", unsafe_allow_html=True)

# Skip email verification - use default customer
if "customer_email" not in st.session_state:
    st.session_state.customer_email = "user@ampere.com"

# Get customer email (bypass verification)
customer_email = st.session_state.customer_email

# Sidebar UI (file upload, reset button, etc.)
sidebar_ui(customer_email)

# Main Chat UI (appears once upload is done)
chat_ui(customer_email)

# Placeholder content for next features
st.markdown("""
<div class="centered-container">
    <h3>Uploaded PDF Details (Placeholder)</h3>
    <p>This section will show parsed results from the uploaded PDF file.</p>

    <h3> Query Response (Placeholder)</h3>
    <p>This section will show Bedrock-powered query answers based on PDF content.</p>
</div>
""", unsafe_allow_html=True)
