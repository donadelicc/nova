from openai import OpenAI
import os
from dotenv import load_dotenv
# import pyttsx3
# import speech_recognition as sr
from pathlib import Path
from langdetect import detect

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
# load_dotenv(dotenv_path)

load_dotenv()

audio_input_folder = os.getenv("AUDIO_INPUT_FOLDER")
text_input_folder = os.getenv("TEXT_INPUT_FOLDER")
if not os.path.exists(audio_input_folder):
    os.makedirs(audio_input_folder)
if not os.path.exists(text_input_folder):
    os.makedirs(text_input_folder)    



async def transcribe_audio(file_name, text_output_file):
    
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
    
    file_path = os.path.join(text_input_folder, text_output_file)
    
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(transcript)
    print("Audio successfullt trascribed. Transcript:")
    print(transcript)
    
async def detect_language(file_name):
    file_path = os.path.join(text_input_folder, file_name)
    with open(file_path, "r") as file:
        text = file.read()
        language = detect(text)
        return language
    
    
async def translate_transcription(file_name):
    
    file_path = os.path.join(text_input_folder, file_name)

    with open(file_path, "r+", encoding="utf-8") as file:
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
        