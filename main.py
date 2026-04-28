import speech_recognition as sr
import logging
import os
from dotenv import load_dotenv
from gtts import gTTS
import google.generativeai as genai
import streamlit as st


# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# -----------------------------
# Logger setup
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
# Speech to Text
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
    audio_path = "speech.mp3"
    tts.save(audio_path)
    return audio_path


# -----------------------------
# Gemini Model
# -----------------------------
def gemini_model(user_input):
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not found in .env file")

    if not user_input:
        return "I could not understand your voice. Please try again."

    genai.configure(api_key=GEMINI_API_KEY)

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(user_input)

    return response.text


# -----------------------------
# Streamlit App
# -----------------------------
def main():
    st.set_page_config(
        page_title="Multilingual AI Assistant",
        page_icon="🎙️",
        layout="centered",
    )

    st.title("🎙️ Multilingual AI Assistant")
    st.write("Speak into your microphone and get an AI-generated voice response.")

    if not GEMINI_API_KEY:
        st.error("GEMINI_API_KEY not found. Please add it inside your .env file.")
        st.stop()

    if st.button("Ask me anything!"):
        with st.spinner("Listening..."):
            text = takeCommand()

        if not text:
            st.warning("Could not understand your voice. Please try again.")
            return

        st.success(f"You said: {text}")

        with st.spinner("Generating response..."):
            response = gemini_model(text)

        with st.spinner("Converting response to speech..."):
            audio_path = text_to_speech(response)

        with open(audio_path, "rb") as audio_file:
            audio_bytes = audio_file.read()

        st.text_area(label="Response:", value=response, height=300)
        st.audio(audio_bytes, format="audio/mp3")

        st.download_button(
            label="Download Speech",
            data=audio_bytes,
            file_name="speech.mp3",
            mime="audio/mp3",
        )


if __name__ == "__main__":
    main()
