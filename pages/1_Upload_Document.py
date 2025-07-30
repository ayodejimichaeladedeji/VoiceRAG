import streamlit as st
import requests

st.set_page_config(page_title="Upload Document", layout="centered")

API_URL = "http://127.0.0.1:8000/api"

st.title("📄 Upload and Embed Academic Document")

uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf", "docx"])

if uploaded_file is not None:
    if st.button("Upload"):
        with st.spinner("Processing..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                response = requests.post(f"{API_URL}/upload_document", files=files)
                response.raise_for_status()
                result = response.json()
                st.success("File processed successfully")
            except Exception as e:
                st.error(f"Failed to upload: {e}")