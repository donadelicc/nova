from openai import OpenAI
import pyaudio
import wave
import os
from dotenv import load_dotenv

audio_input_folder = "audio_input"
text_output_folder = "text_input"
audio_output_folder = "audio_output"

def transcribe_audio(file_name, text_output_file):
    client = OpenAI()
    
    file_path = os.path.join(audio_input_folder, file_name)
    
    audio_file= open(file_path, "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file,
        response_format="text"
        )
    
    file_path = os.path.join(text_output_folder, text_output_file)
    
    with open(file_path, "w") as file:
        file.write(transcript)
    print("Audio successfullt trascribed. Transcript:")
    print(transcript)