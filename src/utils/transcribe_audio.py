from openai import OpenAI
import os
from dotenv import load_dotenv
# import pyttsx3
# import speech_recognition as sr
from pathlib import Path
from langdetect import detect

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

audio_input_folder = os.getenv("AUDIO_INPUT_FOLDER")
text_output_folder = os.getenv("TEXT_OUTPUT_FOLDER")
if not os.path.exists(audio_input_folder):
    os.makedirs(audio_input_folder)
if not os.path.exists(text_output_folder):
    os.makedirs(text_output_folder)    



def transcribe_audio(file_name, text_output_file):
    
    load_dotenv(dotenv_path)
    
    client = OpenAI()
    
    file_path = os.path.join(audio_input_folder, file_name)
    
    audio_file= open(file_path, "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file,
        response_format="text",
        language="no"
        )
    
    file_path = os.path.join(text_output_folder, text_output_file)
    
    with open(file_path, "w") as file:
        file.write(transcript)
    print("Audio successfullt trascribed. Transcript:")
    print(transcript)
    
def detect_language(file_name):
    file_path = os.path.join(text_output_folder, file_name)
    with open(file_path, "r") as file:
        text = file.read()
        language = detect(text)
        return language
    
    
def translate_transcription(file_name):
    
    file_path = os.path.join(text_output_folder, file_name)

    with open(file_path, "r+") as file:
        transkript = file.read()
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Du er en oversetter av feiltranskriberte spørsmål. Oversett spørsmålet til norsk."},
                {"role": "user", "content": f"{transkript}"}
            ],
            temperature=0.2
        )
        new_transkript = response.choices[0].message.content
        file.seek(0)
        file.write(new_transkript)
        file.truncate()
        print("Transkriptet er oversatt")
        
    
        
    
# def transcribe_audio2(filename):
#     engine = pyttsx3.init()
#     recognizer = sr.Recognizer()
#     with sr.AudioFile(filename) as source:
#         audio = recognizer.record(source)
#     try:
#         return recognizer.recognize_google(audio)
#     except:
#         print("Audio file error")
    