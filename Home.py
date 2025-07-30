import requests
import streamlit as st
from audiorecorder import audiorecorder

st.set_page_config(page_title="Voice Tutor", layout="centered")

API_URL = "http://127.0.0.1:8000/api"

st.title("Text & Voice Assistant 📚🎙️")
st.markdown("Ask a question by **typing** or **recording your voice**.")
st.markdown("Use the sidebar to switch between voice query and document upload.")

input_mode = st.radio("Choose input method:", ["Text", "Voice"], horizontal=True)

if input_mode == "Text":
    query = st.text_input("Your question:", placeholder="e.g., What is the main argument of the paper?")
    if st.button("Ask") and query:
        with st.spinner("Sending..."):
            try:
                response = requests.post(
                    API_URL + "/ask_text",
                    data={"question": query},
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                    timeout=30,
                )
                response.raise_for_status()
                result = response.json()
                st.success(result.get("answer", "No answer returned."))
            except Exception as e:
                st.error(f"Error: {e}")

else:
    st.write("Press the microphone button to start recording. Click again to stop.")

    audio = audiorecorder("Click to record", "Click to stop recording")

    if len(audio) > 0:
        st.audio(audio.export().read(), format="audio/wav")

        if st.button("Send recording for transcription"):
            with st.spinner("Sending audio..."):
                try:
                    audio_bytes = audio.export().read()
                    files = {"audio": ("recording.wav", audio_bytes, "audio/wav")}
                    response = requests.post(f"{API_URL}/ask_audio", files=files)
                    response.raise_for_status()
                    result = response.json()
                    st.success(result.get("answer", "No answer returned."))
                except Exception as e:
                    st.error(f"Error sending audio: {e}")