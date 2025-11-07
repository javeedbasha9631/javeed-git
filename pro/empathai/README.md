# EmpathAI — Accessible Companion for All

> Let intelligence make the world kinder.

## Overview
EmpathAI is a Streamlit web app built for the hackathon theme “AI for Good: Inclusion, Empathy & Accessibility”. It provides:

- Real-time sign language to text & speech (basic gestures).
- An empathetic AI chat companion (text & voice input supported).
- Accessibility-first UI with large controls, high contrast and dark/light mode.

This project is a prototype meant to showcase how simple CV and NLP tools can be combined to increase accessibility and empathy.

## Project structure

empathai/
├── app.py                # Main Streamlit app
├── sign_recognition.py   # Gesture detection using Mediapipe + OpenCV
├── chatbot.py            # Empathy AI chatbot logic
├── utils.py              # Helper functions (TTS, voice input)
├── requirements.txt      # Dependencies
└── README.md             # This file

## Installation

1. Create a Python environment (recommended):

   python -m venv .venv
   .venv\Scripts\activate

2. Install dependencies:

   pip install -r requirements.txt

3. Run the app:

   streamlit run app.py

Notes:
- Some features (webcam access, microphone) depend on the platform and browser. In hosted environments like Replit, Streamlit's camera input or direct OpenCV camera may not work; you can upload an image or audio file instead.
- TTS behavior may vary between environments (pyttsx3 works locally; gTTS fallback uses Google TTS and requires internet).

## Features

- Sign Detection: Uses Mediapipe Hands to detect a few sample gestures ("hello", "yes", "no", "thank you"). Shows detected gesture and annotated camera frames. Option to convert detected text to speech.
- Empathy Chatbot: Friendly, supportive chatbot. Uses Transformers if installed (DialoGPT fallback) or a simple rule-based empathic responder. Accepts typed text or uploaded/recorded audio.
- Accessibility: Large buttons, high contrast mode, screen-reader-friendly labels, and voice triggers.
- Text-to-Sign: When a user types text, the app will show placeholder sign icons or descriptions for common words.
- Social Impact: A page describing the project's goals and impact.

## Team & Contribution

Team: Team [Your Team Name]

Contributions welcome — open issues or PRs to add more sign gestures, improve the empathy model, or add full sign-language datasets.

## Social Impact Statement

EmpathAI aims to reduce communication barriers for people with speech or hearing impairments and to provide gentle emotional support. By combining accessible UI design with AI tools, we hope to increase inclusion and empathy in everyday interactions.

> Made with ❤️ by Team [Your Team Name] for AI for Good Hackathon
