# Speak: Your AI Language Companion

## Introduction

Speak is an innovative, open-source language learning application designed
to help users practice and perfect their speaking skills in a new language.
By leveraging the power of AI, Speak simulates realistic conversations,
making language practice accessible and engaging.

## Features

- Real-time voice transcription using Whisper for accuracy in various languages.
- Conversation simulation and language corrections powered by Hugging Face and Ollama LLMs.
- Personalized feedback through voice cloning with the Bark model.
- Intuitive and accessible user interface built with Streamlit.

## Technologies Used

- Python
- Hugging Face Transformers
- Ollama for LLM
- Streamlit for frontend
- SQLite for database management
- Whisper for voice transcription
- Bark model for voice cloning

## Setup and Installation

To get "Speak" running locally:

1. Install Ollama: https://ollama.com/
2. Run: `ollama run qwen:7b-chat`
3. Clone the repository: `git clone https://github.com/5uru/Speak.git`
4. Change directory: `cd Speak`
5. Install required dependencies: `pip install -r requirements.txt`
6. Run the Streamlit application: `streamlit run app.py`

## What's Next for Speak

- [ ] Containerization with Docker for easier deployment and scalability.
- [ ] Expansion of language offerings and personalized learning experiences.
- [ ] Enhancing the community aspect by enabling user contributions and collaborative learning.