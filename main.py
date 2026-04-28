def main():
    st.set_page_config(
        page_title="Multilingual AI Assistant",
        page_icon="🎙️",
        layout="centered"
    )

    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f172a, #1e1b4b, #312e81);
        color: white;
    }

    .hero {
        text-align: center;
        padding: 35px 25px;
        border-radius: 25px;
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255,255,255,0.15);
        box-shadow: 0 20px 50px rgba(0,0,0,0.35);
        margin-bottom: 30px;
    }

    .hero h1 {
        font-size: 44px;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #a78bfa, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero p {
        color: #cbd5e1;
        font-size: 17px;
    }

    div.stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #2563eb, #7c3aed, #db2777);
        color: white;
        border: none;
        border-radius: 40px;
        padding: 15px;
        font-size: 20px;
        font-weight: 700;
        box-shadow: 0 12px 35px rgba(124, 58, 237, 0.45);
    }

    div.stButton > button:hover {
        transform: scale(1.03);
        box-shadow: 0 18px 45px rgba(219, 39, 119, 0.55);
    }

    .result-card {
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 20px;
        padding: 20px;
        margin-top: 20px;
        color: #e5e7eb;
    }

    .footer {
        text-align: center;
        color: #94a3b8;
        margin-top: 35px;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="hero">
        <h1>🎙️ Multilingual AI Assistant</h1>
        <p>Speak your question and get an AI-powered voice response.</p>
        <p><b>Powered by OpenRouter + GPT-OSS-120B Free</b></p>
    </div>
    """, unsafe_allow_html=True)

    if not OPENROUTER_API_KEY:
        st.error("OPENROUTER_API_KEY missing in .env file")
        st.stop()

    if st.button("🎤 Ask me Anything!"):
        with st.spinner("🎧 Listening..."):
            text = takeCommand()

        if not text:
            st.warning("Could not hear you clearly. Please try again.")
            return

        st.markdown(
            f"""
            <div class="result-card">
                <h4>🗣️ You Said</h4>
                <p>{text}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.spinner("🧠 Thinking..."):
            response = llm_response(text)

        st.markdown(
            f"""
            <div class="result-card">
                <h4>🤖 AI Response</h4>
                <p>{response}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.spinner("🔊 Generating voice..."):
            audio_path = text_to_speech(response)

        with open(audio_path, "rb") as f:
            audio_bytes = f.read()

        st.audio(audio_bytes, format="audio/mp3")

        st.download_button(
            label="⬇️ Download Speech",
            data=audio_bytes,
            file_name="speech.mp3",
            mime="audio/mp3"
        )

    st.markdown("""
    <div class="footer">
        Built with Python, Streamlit, SpeechRecognition, gTTS and OpenRouter.
    </div>
    """, unsafe_allow_html=True)
