import os
import logging
import tempfile

import streamlit as st
import speech_recognition as sr
from dotenv import load_dotenv
from gtts import gTTS
from openai import OpenAI


load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "application.log"),
    format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)


def speech_to_text(audio_file):
    recognizer = sr.Recognizer()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(audio_file.read())
        temp_audio_path = temp_audio.name

    try:
        with sr.AudioFile(temp_audio_path) as source:
            audio = recognizer.record(source)

        return recognizer.recognize_google(audio, language="en-in")

    except Exception as e:
        logging.exception(e)
        return None


def llm_response(user_input):
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b:free",
            messages=[
                {
                    "role": "system",
                    "content": "You are a smart, helpful AI voice assistant. Keep answers clear, friendly, and useful."
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            temperature=0.7,
            max_tokens=500
        )

        return response.choices[0].message.content

    except Exception as e:
        logging.exception(e)
        return "Model request failed. Please check your OpenRouter API key or model availability."


def text_to_speech(text):
    tts = gTTS(text=text, lang="en")
    audio_path = "speech.mp3"
    tts.save(audio_path)
    return audio_path


def main():
    st.set_page_config(
        page_title="AI Voice Assistant",
        page_icon="🎙️",
        layout="centered"
    )

    st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at top left, #1d4ed8 0%, #0f172a 35%, #020617 100%);
        color: white;
    }

    .main-card {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.14);
        border-radius: 28px;
        padding: 38px 32px;
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.35);
        backdrop-filter: blur(14px);
        text-align: center;
        margin-top: 20px;
        margin-bottom: 24px;
    }

    .title {
        font-size: 48px;
        font-weight: 900;
        background: linear-gradient(90deg, #38bdf8, #a78bfa, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
    }

    .subtitle {
        color: #cbd5e1;
        font-size: 17px;
        line-height: 1.6;
    }

    .badge-row {
        margin-top: 20px;
    }

    .badge {
        display: inline-block;
        padding: 8px 14px;
        margin: 5px;
        border-radius: 999px;
        background: rgba(56, 189, 248, 0.12);
        border: 1px solid rgba(56, 189, 248, 0.35);
        color: #e0f2fe;
        font-size: 13px;
        font-weight: 600;
    }

    .section-card {
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 22px;
        padding: 22px;
        margin-top: 18px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.25);
    }

    .section-title {
        font-size: 20px;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 10px;
    }

    .section-text {
        color: #dbeafe;
        font-size: 15px;
        line-height: 1.7;
    }

    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 13px;
        margin-top: 32px;
    }

    [data-testid="stAudioInput"] {
        background: rgba(255,255,255,0.08);
        border-radius: 20px;
        padding: 18px;
        border: 1px solid rgba(255,255,255,0.14);
    }

    textarea {
        border-radius: 16px !important;
    }

    .stDownloadButton button {
        background: linear-gradient(90deg, #2563eb, #7c3aed, #db2777);
        color: white;
        border: none;
        border-radius: 999px;
        padding: 12px 24px;
        font-weight: 700;
    }

    .stDownloadButton button:hover {
        transform: scale(1.02);
        box-shadow: 0 10px 30px rgba(124, 58, 237, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="main-card">
        <div class="title">🎙️ Multilingual AI Asssitant</div>
        <div class="subtitle">
            Speak naturally. Get intelligent AI-powered voice responses instantly.
            <br>
            Powered by <b>OpenRouter</b> + <b>GPT-OSS-120B Free</b>
        </div>
        <div class="badge-row">
            <span class="badge">Speech to Text</span>
            <span class="badge">OpenRouter AI</span>
            <span class="badge">Text to Speech</span>
            <span class="badge">Streamlit</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not OPENROUTER_API_KEY:
        st.error("OPENROUTER_API_KEY missing. Add it in Streamlit Secrets.")
        st.stop()

    st.markdown("""
    <div class="section-card">
        <div class="section-title">🎤 Ask me Anything!</div>
        <div class="section-text">
            Record your voice below. The assistant will understand your question, generate a response, and speak it back.
        </div>
    </div>
    """, unsafe_allow_html=True)

    audio_input = st.audio_input("🎙️ Ask me Anything!")

    if audio_input:
        with st.spinner("🎧 Converting your voice to text..."):
            user_text = speech_to_text(audio_input)

        if not user_text:
            st.warning("Could not understand your audio. Please try again.")
            return

        st.markdown(
            f"""
            <div class="section-card">
                <div class="section-title">🗣️ You Said</div>
                <div class="section-text">{user_text}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.spinner("🧠 Thinking..."):
            reply = llm_response(user_text)

        st.markdown("""
        <div class="section-card">
            <div class="section-title">🤖 AI Response</div>
        </div>
        """, unsafe_allow_html=True)

        st.text_area(
            label="",
            value=reply,
            height=250
        )

        with st.spinner("🔊 Generating voice response..."):
            audio_path = text_to_speech(reply)

        with open(audio_path, "rb") as f:
            audio_bytes = f.read()

        st.audio(audio_bytes, format="audio/mp3")

        st.download_button(
            label="⬇️ Download Voice Response",
            data=audio_bytes,
            file_name="speech.mp3",
            mime="audio/mp3"
        )

    st.markdown("""
    <div class="footer">
        Built with Python, Streamlit, SpeechRecognition, gTTS and OpenRouter.
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
