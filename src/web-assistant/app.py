import base64
import os
from dotenv import load_dotenv
import sys

import streamlit as st
import streamlit.components.v1 as components
from pydub import AudioSegment
import io

import speech_recognition as sr

project_root = os.path.join('C:', os.sep, 'Users', 'prebe', 'OneDrive', 'HVL2', 'DAT255', 'Course Project', 'raberrypi_AIassistant')
src_dir = os.path.join(project_root, 'src')

if src_dir not in sys.path:
    sys.path.append(src_dir)

# print(sys.path)  # To verify that the src path has been added

from utils.transcribe_audio import transcribe_audio, detect_language, translate_transcription
from utils.response_handling import response_memory
from utils.text_to_speech import text_to_speech, get_audio_bytes


# Calculate the path to the src directory and add it to sys.path


# Initialize the recognizer
r = sr.Recognizer()

# Streamlit app layout
st.title("Voice Activated Assistant")



def autoplay_audio(file_path):
    audio_base64 = base64.b64encode(open(file_path, 'rb').read()).decode("utf-8")
    audio_html = f"""
    <div style="display: none;">
        <audio controls autoplay>
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
    </div>
    """
    components.html(audio_html, height=50)  




def listen_and_respond():
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as mic:
            print("Please ask your question")
            
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic, timeout=10, snowboy_configuration=None)
            # text = recognizer.recognize_google(audio).lower()
        
            print("Voice detected. Processing...")
            audio_input_folder = os.getenv("AUDIO_INPUT_FOLDER")
            audio_input_file = "audio.wav"
            audio_input = os.path.join(audio_input_folder, audio_input_file)
            
            with open(audio_input, "wb") as f:
                f.write(audio.get_wav_data())
            
            audio_output_folder = os.getenv("AUDIO_OUTPUT_FOLDER")
            text_file = "transcript.txt"
            audio_output_file = "audio.mp3"
            
            transcribe_audio(audio_input_file, text_file)
            transcription_lang = detect_language(text_file)
            
            if transcription_lang != "no":
                print(f"Language detected is {transcription_lang}. Translating...")
                translate_transcription(text_file)
            
            res = response_memory(text_file)
            text_to_speech(res, audio_output_file)
            audio_output_path = audio_output_folder + "/" + audio_output_file
            autoplay_audio(audio_output_path) 
    
    except sr.WaitTimeoutError:
        print("No question detected. You can try asking again.")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")


if st.button("Start Listening"):  # Make the button control the process
# Display listening status
    st.write("Listening...")
    try: 
        listen_and_respond()
    except (sr.WaitTimeoutError, sr.UnknownValueError, sr.RequestError) as e:
        st.error(str(e))  # Display errors appropriately


    

    