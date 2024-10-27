import streamlit as st
import sounddevice as sd
import numpy as np
import speech_recognition as sr
import barcode
from barcode.writer import ImageWriter
import wave

# تابع برای ضبط صدا
def record_audio(duration=10, fs=44100):
    st.write("Recording in progress...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # صبر کنید تا ضبط به اتمام برسد

    # ذخیره صوت به عنوان فایل WAV
    with wave.open("output.wav", 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit PCM
        wf.setframerate(fs)
        wf.writeframes(audio.tobytes())

    return "output.wav"

# تابع برای تبدیل صدا به متن
def recognize_speech(audio_file):
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        
    try:
        text = recognizer.recognize_google(audio_data, language="en-US")
        return text.upper()
    except sr.UnknownValueError:
        return "Sorry, I cannot understand the recorded audio."
    except sr.RequestError:
        return "Results were not requested from the Google speech recognition service."

# تابع برای تبدیل متن به بارکد
def generate_barcode(text):
    code128 = barcode.get('code128', text, writer=ImageWriter())
    filename = 'barcode'
    code128.save(filename)
    return filename + '.png'

# رابط کاربری با Streamlit
st.title("Speech to Text")
st.write("Press the button below to start speaking.")

# دکمه ضبط صدا
if st.button("Start Recording"):
    audio_file = record_audio()  # ضبط صدا
    text = recognize_speech(audio_file)  # تبدیل صدا به متن
    st.write("Converted text (in uppercase):")
    
    if 'recognized_text' not in st.session_state:
        st.session_state.recognized_text = text

# ویرایش متن شناسایی‌شده
if 'recognized_text' in st.session_state:
    edited_text = st.text_input("Edit the text:", value=st.session_state.recognized_text)
    
    if st.button("Generate Barcode"):
        barcode_image = generate_barcode(edited_text)
        st.write("Generated barcode:")
        st.image(barcode_image)
