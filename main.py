import os
import logging
import speech_recognition as sr
import streamlit as st

from dotenv import load_dotenv
from gtts import gTTS
from openai import OpenAI


load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


# -----------------------------
# Logging
# -----------------------------
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "application.log"),
    format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


# -----------------------------
# OpenRouter Client
# -----------------------------
client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)


# -----------------------------
# Speech Recognition
# -----------------------------
def takeCommand():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            recognizer.pause_threshold = 1
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

        query = recognizer.recognize_google(audio, language="en-in")
        return query

    except Exception as e:
        logging.exception(e)
        return None


# -----------------------------
# LLM Response
# -----------------------------
def llm_response(user_input):
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b:free",
            messages=[
                {
                    "role": "system",
                    "content": "You are a smart, helpful multilingual AI voice assistant. Keep answers clear, friendly, and useful."
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
        return "Unable to generate response right now. Please check your OpenRouter API key or try again later."


# -----------------------------
# Text to Speech
# -----------------------------
def text_to_speech(text):
    audio_path = "speech.mp3"
    tts = gTTS(text=text, lang="en")
    tts.save(audio_path)
    return audio_path


# -----------------------------
# Streamlit App
# -----------------------------
def main():
    st.set_page_config(
        page_title="Multilingual AI Assistant",
        page_icon="🎙️",
        layout="centered"
    )

    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 45%, #312e81 100%);
            color: white;
        }

        .main-card {
            background: rgba(255, 255, 255, 0.08);
            padding: 35px;
            border-radius: 24px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.35);
            border: 1px solid rgba(255,255,255,0.15);
            backdrop-filter: blur(12px);
            text-align: center;
            margin-top: 20px;
        }

        .title {
            font-size: 48px;
            font-weight: 800;
            background: linear-gradient(90deg, #38bdf8, #a78bfa, #f472b6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }

        .subtitle {
            font-size: 18px;
            color: #cbd5e1;
            margin-bottom: 25px;
        }

        .status-box {
            background: rgba(255,255,255,0.1);
            padding: 18px;
            border-radius: 16px;
            border-left: 5px solid #38bdf8;
            margin: 15px 0;
            text-align: left;
        }

        .response-box {
            background: rgba(15, 23, 42, 0.75);
            padding: 22px;
            border-radius: 18px;
            border: 1px solid rgba(255,255,255,0.12);
            color: #e5e7eb;
            line-height: 1.6;
            margin-top: 20px;
            text-align: left;
        }

        div.stButton > button {
            background: linear-gradient(90deg, #2563eb, #7c3aed, #db2777);
            color: white;
            border: none;
            padding: 14px 34px;
            border-radius: 40px;
            font-size: 18px;
            font-weight: 700;
            box-shadow: 0 10px 30px rgba(124, 58, 237, 0.45);
            transition: all 0.3s ease;
        }

        div.stButton > button:hover {
            transform: scale(1.05);
            box-shadow: 0 15px 40px rgba(219, 39, 119, 0.55);
        }

        .footer {
            text-align: center;
            color: #94a3b8;
            margin-top: 30px;
            font-size: 14px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if not OPENROUTER_API_KEY:
        st.error("OPENROUTER_API_KEY missing. Add it in your .env file or Streamlit secrets.")
        st.stop()

    st.markdown(
        """
        <div class="main-card">
            <div class="title">🎙️ Multilingual AI Assistant</div>
            <div class="subtitle">
                Speak naturally. Get intelligent AI-powered voice responses.
                <br>
                Powered by <b>OpenRouter</b> + <b>GPT-OSS-120B Free</b>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        ask_button = st.button("🎤 Ask me Anything!")

    if ask_button:
        with st.spinner("🎧 Listening to your voice..."):
            text = takeCommand()

        if not text:
            st.warning("I could not hear you clearly. Please try again.")
            return

        st.markdown(
            f"""
            <div class="status-box">
                <b>🗣️ You said:</b><br>
                {text}
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.spinner("🧠 Thinking..."):
            response = llm_response(text)

        st.markdown(
            f"""
            <div class="response-box">
                <b>🤖 AI Response:</b><br><br>
                {response}
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.spinner("🔊 Creating voice response..."):
            audio_path = text_to_speech(response)

        with open(audio_path, "rb") as f:
            audio_bytes = f.read()

        st.audio(audio_bytes, format="audio/mp3")

        st.download_button(
            label="⬇️ Download Voice Response",
            data=audio_bytes,
            file_name="speech.mp3",
            mime="audio/mp3"
        )

    st.markdown(
        """
        <div class="footer">
            Built with Python, Streamlit, Speech Recognition, gTTS and OpenRouter.
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
