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

        text = recognizer.recognize_google(audio, language="en-in")
        return text

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

    st.title("🎙️ Multilingual AI Assistant")
    st.write("Powered by OpenRouter + GPT-OSS-120B Free")

    if not OPENROUTER_API_KEY:
        st.error("OPENROUTER_API_KEY missing. Add it in Streamlit Secrets.")
        st.stop()

    audio_input = st.audio_input("Record your voice")

    if audio_input:
        with st.spinner("Converting speech to text..."):
            user_text = speech_to_text(audio_input)

        if not user_text:
            st.warning("Could not understand your audio. Please try again.")
            return

        st.success(f"You said: {user_text}")

        with st.spinner("Thinking..."):
            reply = llm_response(user_text)

        st.text_area("AI Response", reply, height=250)

        with st.spinner("Generating voice..."):
            audio_path = text_to_speech(reply)

        with open(audio_path, "rb") as f:
            audio_bytes = f.read()

        st.audio(audio_bytes, format="audio/mp3")

        st.download_button(
            label="Download Speech",
            data=audio_bytes,
            file_name="speech.mp3",
            mime="audio/mp3"
        )


if __name__ == "__main__":
    main()
