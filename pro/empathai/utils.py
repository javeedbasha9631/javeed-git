"""
utils.py

Helper functions: text-to-speech (pyttsx3 and gTTS fallback), transcribe uploaded audio using SpeechRecognition.
"""
import io
import os
import tempfile
import threading
from typing import Optional

import streamlit as st

try:
    import pyttsx3
except Exception:
    pyttsx3 = None

try:
    from gtts import gTTS
except Exception:
    gTTS = None

try:
    import speech_recognition as sr
except Exception:
    sr = None

from pydub import AudioSegment


def speak_text(text: str) -> Optional[bytes]:
    """Speak text and return audio bytes (mp3) for Streamlit playback.

    Tries pyttsx3 first (may play locally), otherwise uses gTTS to create an mp3 and returns its bytes.
    """
    if not text:
        return None

    # Try pyttsx3 if available (local TTS)
    if pyttsx3 is not None:
        try:
            engine = pyttsx3.init()
            # Run in a background thread so Streamlit doesn't block when used locally
            def _speak():
                engine.say(text)
                engine.runAndWait()

            threading.Thread(target=_speak, daemon=True).start()
            return None
        except Exception:
            pass

    # Fallback to gTTS
    if gTTS is not None:
        try:
            tts = gTTS(text=text, lang="en")
            buf = io.BytesIO()
            tts.write_to_fp(buf)
            buf.seek(0)
            return buf.read()
        except Exception:
            return None

    return None


def transcribe_audio_file(uploaded_file) -> str:
    """Transcribe an uploaded audio file (wav, mp3, etc.) using SpeechRecognition.

    Returns recognized text or empty string.
    """
    if sr is None:
        return ""  # SpeechRecognition not installed

    recognizer = sr.Recognizer()

    # Convert uploaded file to WAV using pydub for compatibility
    try:
        audio_bytes = uploaded_file.read()
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes))
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            audio.export(f.name, format="wav")
            tmpname = f.name

        with sr.AudioFile(tmpname) as source:
            audio_data = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            text = ""
        except sr.RequestError:
            text = ""

        try:
            os.unlink(tmpname)
        except Exception:
            pass

        return text
    except Exception:
        return ""


def ensure_bytes_to_streamlit_audio(maybe_bytes: Optional[bytes]):
    """If bytes provided, returns (audio_bytes, 'audio/mp3') else (None, None).
    Streamlit can play raw bytes with st.audio.
    """
    if not maybe_bytes:
        return None
    return maybe_bytes
