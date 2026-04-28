<h1 align="center">🎙️ Multilingual AI Assistant</h1>

<p align="center">
  A Python + Streamlit based voice assistant that listens to your voice, converts speech to text, sends the query to OpenRouter, generates an AI response using <strong>openai/gpt-oss-120b:free</strong>, and converts the response back into speech.
</p>

<hr>

<h2>🚀 Features</h2>

<ul>
  <li>Voice input using microphone</li>
  <li>Speech-to-text using Google Speech Recognition</li>
  <li>AI response generation using OpenRouter</li>
  <li>Uses <code>openai/gpt-oss-120b:free</code> model</li>
  <li>Text-to-speech using gTTS</li>
  <li>Streamlit web interface</li>
  <li>Audio playback inside browser</li>
  <li>Download generated response as MP3</li>
  <li>Application logging for debugging</li>
</ul>

<h2>🛠️ Tech Stack</h2>

<ul>
  <li>Python</li>
  <li>Streamlit</li>
  <li>OpenRouter API</li>
  <li>OpenAI Python SDK</li>
  <li>SpeechRecognition</li>
  <li>gTTS</li>
  <li>python-dotenv</li>
  <li>PyAudio</li>
</ul>

<h2>📁 Project Structure</h2>

<pre>
AI-Voice-Assistant/
│
├── main.py
├── .env
├── requirements.txt
├── logs/
│   └── application.log
├── speech.mp3
└── README.md
</pre>

<h2>🔐 Environment Variables</h2>

<p>Create a <code>.env</code> file in the project root:</p>

<pre>
OPENROUTER_API_KEY=your_openrouter_api_key_here
</pre>

<h2>📦 Installation</h2>

<pre>
git clone https://github.com/your-username/AI-Voice-Assistant.git
cd AI-Voice-Assistant
</pre>

<pre>
pip install -r requirements.txt
</pre>

<h2>📌 requirements.txt</h2>

<pre>
streamlit
python-dotenv
SpeechRecognition
gTTS
openai
pyaudio
</pre>

<h2>▶️ How to Run</h2>

<pre>
streamlit run main.py
</pre>

<h2>🎯 How It Works</h2>

<ol>
  <li>User clicks <strong>Ask Me Anything</strong>.</li>
  <li>The app listens through the microphone.</li>
  <li>Speech is converted into text using SpeechRecognition.</li>
  <li>The text is sent to OpenRouter API.</li>
  <li>The model <code>openai/gpt-oss-120b:free</code> generates a response.</li>
  <li>The response is converted into speech using gTTS.</li>
  <li>The generated audio is played inside Streamlit.</li>
  <li>User can download the response as an MP3 file.</li>
</ol>

<h2>🎙️ Example Use Cases</h2>

<ul>
  <li>Voice-based AI assistant</li>
  <li>Personal productivity assistant</li>
  <li>AI chatbot with speech output</li>
  <li>Accessibility-friendly assistant</li>
  <li>Beginner-friendly GenAI project</li>
</ul>

<h2>⚠️ Common Issues</h2>

<h3>PyAudio Installation Error</h3>

<p>If PyAudio fails on Windows, try using Python 3.8, 3.10, or 3.11.</p>

<pre>
pip install pipwin
pipwin install pyaudio
</pre>

<h3>OpenRouter API Key Error</h3>

<p>Make sure your <code>.env</code> file contains:</p>

<pre>
OPENROUTER_API_KEY=your_actual_openrouter_key
</pre>

<h3>Microphone Not Working</h3>

<ul>
  <li>Check microphone permission</li>
  <li>Check Windows input device settings</li>
  <li>Make sure PyAudio is installed correctly</li>
</ul>

<h3>Model Request Failed</h3>

<ul>
  <li>Check your OpenRouter API key</li>
  <li>Check if the free model is available</li>
  <li>Check your internet connection</li>
  <li>Try again after a few seconds</li>
</ul>

<h2>🔮 Future Improvements</h2>

<ul>
  <li>Add conversation memory</li>
  <li>Add multilingual voice output</li>
  <li>Add wake word detection</li>
  <li>Add Whisper-based speech recognition</li>
  <li>Add RAG support with LangChain</li>
  <li>Add browser search and tool calling</li>
  <li>Add local file reading capability</li>
  <li>Deploy on cloud</li>
</ul>

<h2>👨‍💻 Author</h2>

<p>
  Developed by <strong>Rishav Patel</strong>
</p>

<h2>📌 Project Status</h2>

<p>
  This project is a beginner-friendly AI voice assistant built to demonstrate speech recognition,
  OpenRouter API integration, generative AI response generation, text-to-speech, and Streamlit-based deployment.
</p>

<hr>

<h3 align="center">
  ⭐ If you like this project, consider giving it a star on GitHub!
</h3>
