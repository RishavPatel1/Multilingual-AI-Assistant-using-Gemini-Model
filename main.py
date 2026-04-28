import speech_recognition as sr
import logging
import os
from dotenv import load_dotenv
from gtts import gTTS
import streamlit as st
from openai import OpenAI


# -----------------------------
# Load ENV
# -----------------------------
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


# -----------------------------
# Logger
# -----------------------------
LOG_DIR = "logs"
LOG_FILE_NAME = "application.log"

os.makedirs(LOG_DIR, exist_ok=True)

log_path = os.path.join(LOG_DIR, LOG_FILE_NAME)

logging.basicConfig(
    filename=log_path,
    format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


# -----------------------------
# OpenRouter Client
# -----------------------------
client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)


# -----------------------------
# Voice Input
# -----------------------------
def takeCommand():
    r = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            st.info("Listening...")
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, duration=0.5)

            audio = r.listen(source, timeout=5, phrase_time_limit=10)

        st.info("Recognizing...")
        query = r.recognize_google(audio, language="en-in")

        return query

    except Exception as e:
        logging.info(e)
        return None


# -----------------------------
# Text to Speech
# -----------------------------
def text_to_speech(text):
    tts = gTTS(text=text, lang="en")
    file_path = "speech.mp3"
    tts.save(file_path)
    return file_path


# -----------------------------
# OpenRouter Model
# -----------------------------
def llm_response(user_input):
    if not OPENROUTER_API_KEY:
        return "OPENROUTER_API_KEY missing in .env file."

    if not user_input:
        return "I could not understand your voice."

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b:free",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI voice assistant."
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
        return "Model request failed. Please check OpenRouter API key or free model availability."


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
    st.write("Powered by OpenRouter + GPT-OSS-120B")

    if not OPENROUTER_API_KEY:
        st.error("OPENROUTER_API_KEY missing in .env file")
        st.stop()

    if st.button("Ask Me Anything"):
        with st.spinner("Listening..."):
            user_text = takeCommand()

        if not user_text:
            st.warning("Could not hear you properly.")
            return

        st.success(f"You said: {user_text}")

        with st.spinner("Thinking..."):
            reply = llm_response(user_text)

        with st.spinner("Generating voice..."):
            audio_path = text_to_speech(reply)

        with open(audio_path, "rb") as f:
            audio_bytes = f.read()

        st.text_area("Response", reply, height=250)
        st.audio(audio_bytes, format="audio/mp3")

        st.download_button(
            label="Download Voice",
            data=audio_bytes,
            file_name="speech.mp3",
            mime="audio/mp3"
        )


if __name__ == "__main__":
    main()
