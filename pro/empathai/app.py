"""
app.py

Streamlit front-end for EmpathAI — integrates sign recognition, empathy chatbot and accessibility controls.
"""
import streamlit as st
import time
import io
import cv2
import numpy as np

from sign_recognition import detect_sign_from_frame
from chatbot import EmpathyChatbot
from utils import speak_text, transcribe_audio_file, ensure_bytes_to_streamlit_audio


st.set_page_config(page_title="EmpathAI — Accessible Companion", layout="wide")


def inject_css(large_font=False, high_contrast=False, dark_mode=False):
    bg = "#0f1720" if dark_mode else "#ffffff"
    fg = "#ffffff" if dark_mode else "#000000"
    contrast = "-webkit-text-stroke: 0.6px black;" if high_contrast else ""
    font_size = "20px" if large_font else "16px"
    css = f"""
    <style>
    .big-title {{font-size:32px; font-weight:700;}}
    html, body, [class*="stApp"] {{ background: {bg}; color: {fg}; }}
    .stButton>button {{ font-size: {font_size}; padding: 12px 18px; }}
    .stTextInput>div>input, .stTextArea>div>textarea {{ font-size: {font_size}; }}
    .stMarkdown {{ {contrast} }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def main():
    # Sidebar accessibility settings
    st.sidebar.title("Accessibility Settings")
    dark_mode = st.sidebar.checkbox("Dark mode", value=False)
    high_contrast = st.sidebar.checkbox("High contrast", value=True)
    large_font = st.sidebar.checkbox("Large font", value=True)
    voice_trigger = st.sidebar.checkbox("Enable voice commands (upload audio)", value=False)

    inject_css(large_font=large_font, high_contrast=high_contrast, dark_mode=dark_mode)

    st.markdown("<div class='big-title'>EmpathAI — Accessible Companion for All</div>", unsafe_allow_html=True)
    st.markdown("**Let intelligence make the world kinder.**")

    # Navigation
    st.write("\n")
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        if st.button("Start Sign Detection"):
            st.session_state['page'] = 'sign'
    with col2:
        if st.button("Chat with EmpathAI"):
            st.session_state['page'] = 'chat'
    with col3:
        if st.button("Learn Our Impact"):
            st.session_state['page'] = 'impact'

    page = st.session_state.get('page', 'home')

    if page == 'home':
        st.header("Welcome")
        st.write("Choose a mode above to begin. You can use sign detection to translate gestures, or chat with an empathetic AI companion.")
        st.markdown("### Quick demo")
        st.write("Try: 'I'm feeling anxious' in Chat, or Start Sign Detection and hold up an open palm for 'hello'.")

    if page == 'sign':
        st.header("Sign Detection — Live & Snapshot Modes")
        st.markdown("Instructions: Allow camera access or upload a photo. Sample gestures detected: hello, yes, no, thank you.")
        colA, colB = st.columns([2,1])
        with colA:
            use_live = st.checkbox("Use live OpenCV camera (may not work in hosted env)", value=False)
            if use_live:
                st.write("Starting live camera. Press Stop to end.")
                run_key = 'sign_live_running'
                if run_key not in st.session_state:
                    st.session_state[run_key] = False

                if st.button("Start Live"):
                    st.session_state[run_key] = True

                if st.button("Stop Live"):
                    st.session_state[run_key] = False

                placeholder = st.empty()
                cap = None
                if st.session_state[run_key]:
                    cap = cv2.VideoCapture(0)
                    if not cap.isOpened():
                        st.error("Unable to access camera via OpenCV. Try using the snapshot camera below.")
                    else:
                        while st.session_state[run_key]:
                            ret, frame = cap.read()
                            if not ret:
                                break
                            label, ann = detect_sign_from_frame(frame)
                            ann_rgb = cv2.cvtColor(ann, cv2.COLOR_BGR2RGB)
                            placeholder.image(ann_rgb, use_column_width=True)
                            st.write(f"Detected: **{label}**")
                            time.sleep(0.05)
                        cap.release()

            else:
                uploaded = st.camera_input("Use your browser camera (snapshot) or upload an image")
                if uploaded is not None:
                    # Read image bytes into OpenCV format
                    file_bytes = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)
                    img = cv2.imdecode(file_bytes, 1)
                    label, ann = detect_sign_from_frame(img)
                    ann_rgb = cv2.cvtColor(ann, cv2.COLOR_BGR2RGB)
                    st.image(ann_rgb, use_column_width=True)
                    st.success(f"Detected: {label}")

        with colB:
            st.markdown("### Detected text to speech")
            if st.button("Speak last detected"):
                # For the demo, ask for manual input to speak
                to_speak = st.text_input("Text to speak", value="Hello — this is EmpathAI.")
                audio_bytes = speak_text(to_speak)
                if audio_bytes:
                    st.audio(audio_bytes, format='audio/mp3')

            st.markdown("### Text-to-Sign (demo)")
            text = st.text_input("Type text to see sign placeholders", value="hello")
            if text:
                words = [w.strip().lower() for w in text.split()]
                for w in words:
                    # In a real app, show images. Here we show placeholder text/emoji.
                    if w in ['hello']:
                        st.write(f"{w}: 👋  (open palm)")
                    elif w in ['yes', 'yeah']:
                        st.write(f"{w}: 👍  (thumbs up)")
                    elif w in ['no']:
                        st.write(f"{w}: ✊  (closed fist)")
                    elif w in ['thank', 'thankyou', 'thank you'] or w.startswith('thank'):
                        st.write(f"{w}: 🙏  (thank you - approximate)")
                    else:
                        st.write(f"{w}: [sign placeholder]")

    if page == 'chat':
        st.header("Chat with EmpathAI")
        st.markdown("An empathetic companion — type or upload audio. Try expressing how you feel.")
        bot = EmpathyChatbot()

        if voice_trigger:
            uploaded_audio = st.file_uploader("Upload a short audio clip (wav/mp3) to transcribe and send to the bot", type=["wav", "mp3", "m4a"])
            if uploaded_audio is not None:
                with st.spinner("Transcribing audio..."):
                    text = transcribe_audio_file(uploaded_audio)
                st.success(f"You said: {text}")
                reply = bot.respond(text)
                st.markdown(f"**EmpathAI:** {reply}")
                # speak reply
                audio_bytes = speak_text(reply)
                if audio_bytes:
                    st.audio(audio_bytes, format='audio/mp3')

        user_input = st.text_area("Your message", value="", height=120)
        if st.button("Send") and user_input.strip():
            with st.spinner("Thinking..."):
                reply = bot.respond(user_input)
            st.markdown(f"**You:** {user_input}")
            st.markdown(f"**EmpathAI:** {reply}")
            audio_bytes = speak_text(reply)
            if audio_bytes:
                st.audio(audio_bytes, format='audio/mp3')

    if page == 'impact':
        st.header("Our Social Impact")
        st.markdown("EmpathAI supports inclusion by lowering communication barriers and offering empathetic support.")
        st.write("Key points:")
        st.write("- Accessibility-first UI with large controls and voice options")
        st.write("- Sign detection helps people with hearing or speech differences communicate")
        st.write("- Empathetic chatbot provides a non-judgmental companion for mental wellness check-ins")
        st.markdown("---")
        st.markdown("Let intelligence make the world kinder.")


if __name__ == '__main__':
    main()
