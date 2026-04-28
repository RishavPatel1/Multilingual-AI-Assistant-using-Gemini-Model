<h1 align="center">🎙️ Multilingual AI Voice Assistant</h1>

<p align="center">
  A Python + Streamlit based AI voice assistant that listens to your voice, converts speech to text, generates intelligent responses using Google Gemini, and converts the response back into speech.
</p>

<hr>

<h2>🚀 Features</h2>

<ul>
  <li>Voice input using microphone</li>
  <li>Speech-to-text using Google Speech Recognition</li>
  <li>AI response generation using Google Gemini</li>
  <li>Text-to-speech using gTTS</li>
  <li>Audio playback inside Streamlit</li>
  <li>Download generated speech as MP3</li>
  <li>Error logging for debugging</li>
  <li>Clean Streamlit web interface</li>
</ul>

<h2>🛠️ Tech Stack</h2>

<ul>
  <li>Python</li>
  <li>Streamlit</li>
  <li>Google Gemini API</li>
  <li>SpeechRecognition</li>
  <li>gTTS</li>
  <li>python-dotenv</li>
  <li>Logging</li>
</ul>

<h2>📁 Project Structure</h2>

<pre>
Multilingual-AI-Assistant/
│
├── main.py
├── .env
├── requirements.txt
├── logs/
│   └── application.log
└── README.md
</pre>

<h2>🔐 Environment Variables</h2>

<p>Create a <code>.env</code> file in the project root:</p>

<pre>
GEMINI_API_KEY=your_gemini_api_key_here
</pre>

<h2>📦 Installation</h2>

<pre>
git clone https://github.com/your-username/Multilingual-AI-Assistant.git
cd Multilingual-AI-Assistant
</pre>

<pre>
pip install -r requirements.txt
</pre>

<h2>📌 requirements.txt</h2>

<pre>
streamlit
python-dotenv
google-generativeai
SpeechRecognition
gTTS
pyaudio
</pre>

<h2>▶️ How to Run</h2>

<pre>
streamlit run main.py
</pre>

<h2>🎯 How It Works</h2>

<ol>
  <li>User clicks <strong>Ask me anything</strong>.</li>
  <li>The app listens through the microphone.</li>
  <li>Speech is converted into text.</li>
  <li>The text is sent to Google Gemini.</li>
  <li>Gemini generates an AI response.</li>
  <li>The response is converted into speech using gTTS.</li>
  <li>The user can listen to or download the MP3 response.</li>
</ol>

<h2>🎙️ Example Use Cases</h2>

<ul>
  <li>Ask general knowledge questions</li>
  <li>Voice-based AI chatbot</li>
  <li>Personal assistant prototype</li>
  <li>Language learning assistant</li>
  <li>Accessibility-focused voice assistant</li>
</ul>

<h2>⚠️ Common Issues</h2>

<h3>PyAudio Installation Error</h3>

<p>If PyAudio fails on Windows, try using Python 3.8, 3.10, or 3.11.</p>

<pre>
pip install pipwin
pipwin install pyaudio
</pre>

<h3>Gemini API Key Error</h3>

<p>Make sure your <code>.env</code> file contains:</p>

<pre>
GEMINI_API_KEY=your_actual_key
</pre>

<h3>Microphone Not Working</h3>

<ul>
  <li>Check microphone permission</li>
  <li>Check Windows input device settings</li>
  <li>Make sure PyAudio is installed correctly</li>
</ul>

<h2>🔮 Future Improvements</h2>

<ul>
  <li>Add Hindi and multilingual voice output</li>
  <li>Add conversation memory</li>
  <li>Add wake word detection</li>
  <li>Add local Whisper speech recognition</li>
  <li>Add LangChain / RAG support</li>
  <li>Add tools like weather, browser search, and file reading</li>
  <li>Deploy the app on cloud</li>
</ul>

<h2>👨‍💻 Author</h2>

<p>
  Developed by <strong>Rishav Patel</strong>
</p>

<h2>📌 Project Status</h2>

<p>
  This project is a beginner-friendly AI voice assistant built to demonstrate speech recognition,
  generative AI integration, text-to-speech, and Streamlit-based deployment.
</p>

<hr>

<h3 align="center">
  ⭐ If you like this project, consider giving it a star on GitHub!
</h3>
