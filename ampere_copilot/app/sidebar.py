import streamlit as st
import os
from supabase_client import upload_pdf_to_supabase, process_pdf_data

def sidebar_ui(customer_email: str):
    st.sidebar.title("PDF Upload")
    
    # Email display
    st.sidebar.info(f"Logged in as: {customer_email}")
    
    # PDF Upload - Only PDF files up to 5MB
    uploaded_file = st.sidebar.file_uploader(
        "Upload PDF Document", 
        type=["pdf"],
        help="Upload PDF files only (max 5MB)"
    )
    
    if uploaded_file is not None:
        # Check file size (5MB = 5 * 1024 * 1024 bytes)
        file_size = len(uploaded_file.getbuffer())
        max_size = 5 * 1024 * 1024  # 5MB
        
        if file_size > max_size:
            st.sidebar.error(f"File too large! {file_size / (1024*1024):.2f}MB exceeds 5MB limit")
        else:
            st.sidebar.success(f"Uploaded: {uploaded_file.name} ({file_size / (1024*1024):.2f}MB)")
            
            # Process PDF button
            if st.sidebar.button("Process PDF"):
                with st.spinner("Processing PDF..."):
                    try:
                        # Upload to Supabase
                        file_url = upload_pdf_to_supabase(uploaded_file, customer_email)
                        
                        # Process PDF data
                        pdf_data = process_pdf_data(uploaded_file, customer_email)
                        
                        st.sidebar.success("PDF processed successfully!")
                        st.session_state.pdf_processed = True
                        st.session_state.pdf_data = pdf_data
                        
                    except Exception as e:
                        st.sidebar.error(f"Error processing PDF: {str(e)}")

    # Email reset button
    if st.sidebar.button("Reset Email"):
        st.session_state.email_verified = False
        st.session_state.customer_email = ""
        st.session_state.pdf_processed = False
        st.rerun()
