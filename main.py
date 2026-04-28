import os
import logging
import speech_recognition as sr
import streamlit as st

from dotenv import load_dotenv
from gtts import gTTS
from openai import OpenAI


# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


# -----------------------------
# Logging Setup
# -----------------------------
LOG_DIR = "logs"
LOG_FILE = "application.log"

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, LOG_FILE),
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
            st.info("🎤 Listening...")
            recognizer.pause_threshold = 1
            recognizer.adjust_for_ambient_noise(source, duration=0.5)

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=10
            )

        st.info("🧠 Recognizing...")
        query = recognizer.recognize_google(audio, language="en-in")

        return query

    except Exception as e:
        logging.exception(e)
        return None


# -----------------------------
# OpenRouter LLM Response
# -----------------------------
def llm_response(user_input):
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b:free",
            messages=[
                {
                    "role": "system",
                    "content": "You are a smart multilingual AI voice assistant. Keep answers clear and helpful."
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
        return "Unable to generate response right now. Please try again later."


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

    st.title("🎙️ Multilingual AI Assistant")
    st.write("Powered by OpenRouter + GPT-OSS-120B Free")

    if not OPENROUTER_API_KEY:
        st.error("OPENROUTER_API_KEY missing in .env file")
        st.stop()

    if st.button("Ask me Anything!"):
        with st.spinner("Listening..."):
            text = takeCommand()

        if not text:
            st.warning("Could not hear you clearly. Please try again.")
            return

        st.success(f"You said: {text}")

        with st.spinner("Thinking..."):
            response = llm_response(text)

        st.text_area(
            label="AI Response",
            value=response,
            height=250
        )

        with st.spinner("Generating voice..."):
            audio_path = text_to_speech(response)

        with open(audio_path, "rb") as f:
            audio_bytes = f.read()

        st.audio(audio_bytes, format="audio/mp3")

        st.download_button(
            label="Download Speech",
            data=audio_bytes,
            file_name="speech.mp3",
            mime="audio/mp3"
        )


# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    main()
