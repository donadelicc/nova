from openai import OpenAI
import pyaudio
import wave
import os
from dotenv import load_dotenv
import pyttsx3
import speech_recognition as sr
import openai


audio_input_folder = "audio_input"
text_output_folder = "text_input"
audio_output_folder = "audio_output"

engine = pyttsx3.init()

def transcribe_audio2(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print("Audio file error")
    

def transcribe_audio_openai(file_name, text_output_file):
    
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
    
    
    
def transcribe_audio_azure(file_name, text_output_file):
    
    #load_dotenv()
    
    openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
    openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")  # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
    openai.api_type = "azure"
    openai.api_version = "2023-09-01-preview"
    
    model_name = "whisper"
    deployment_id = "whisper" #This will correspond to the custom name you chose for your deployment when you deployed a model."
    audio_language="no"
    
    file_path = os.path.join(audio_input_folder, file_name)
    
    audio_file= open(file_path, "rb")
    transcript = openai.Audio.transcribe( 
        file=audio_file,
        model=model_name,
        deployment_id=deployment_id,
        language=audio_language
        )
    
    file_path = os.path.join(text_output_folder, text_output_file)
    
    with open(file_path, "w") as file:
        file.write(transcript)
    print("Audio successfullt trascribed. Transcript:")
    print(transcript)
