import streamlit as st

def chat_ui(customer_email: str):
    col1, col2 = st.columns([1, 6])
    with col1:
        import os
        image_path = os.path.join(os.path.dirname(__file__), "ampere_logo.png")
        if os.path.exists(image_path):
            st.image(image_path, width=150)
        else:
            st.warning(f"Image not found at {image_path}")
    with col2:
        st.title("Ampere Copilot Chat")

    if "chat_input" not in st.session_state:
        st.session_state.chat_input = ""
    
    # Container for chat history and results centered on the page
    chat_container = st.container()
    chat_container.markdown("**Chatbot response will appear here.**")
    chat_container.markdown(
        """
        <style>
        .chat-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 60vh;
            border: 1px solid #ddd;
            padding: 10px;
            margin-bottom: 20px;
            overflow-y: auto;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    chat_container.markdown('<div class="chat-container" id="chat-history"></div>', unsafe_allow_html=True)

    # Placeholder for chat input at the bottom of the page
    input_container = st.container()
    with input_container:
        user_input = st.text_input("Enter your query:", key="chat_input")
        if user_input:
            # Display user query and placeholder for chatbot response
            chat_container.markdown(f"**User query:** {user_input}")
            chat_container.markdown("**Chatbot response will appear here.**")
            # Clear input after submission
            # Removed resetting st.session_state.chat_input here to avoid Streamlit error
