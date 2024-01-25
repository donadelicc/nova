from openai import OpenAI
import pyaudio
import wave
import os
from dotenv import load_dotenv

## Set denne til å være i samme mappe som .env filen (burde ligge i roten av prosjektet)
## Denne filen inneholder API nøkkel for OpenAI
load_dotenv(dotenv_path="../.env")

# Definer parametere for opptak
chunk = 1024  # Record in chunks
format = pyaudio.paInt16  # 16 bit format
channels = 1  # mono
sample_rate = 44100  # Sample rate
record_seconds = 10  # Record duration

audio_output_folder = "audio_files"
text_outut_folder = "text_files"

if not os.path.exists(audio_output_folder):
    os.makedirs(audio_output_folder)
if not os.path.exists(text_outut_folder):
    os.makedirs(text_outut_folder)
    

def record_audio(file_name):
    p = pyaudio.PyAudio()

    # Åpne stream for opptak
    stream = p.open(format=format,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=chunk)

    print("Recording...")

    frames = []

    # Opptak av data fra mikrofonen
    for i in range(0, int(sample_rate / chunk * record_seconds)):
        data = stream.read(chunk)
        frames.append(data)
        
    # Stopper og lukker streamen
    stream.stop_stream()
    stream.close()
    p.terminate()

    file_path = os.path.join(audio_output_folder, file_name)

    # Lagrer opptaket til en fil
    wf = wave.open(file_path, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    return file_path


def transcribe_audio(file_name, text_output_file):
    client = OpenAI()
    
    file_path = os.path.join(audio_output_folder, file_name)
    
    audio_file= open(file_path, "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file,
        response_format="text"
        )
    
    file_path = os.path.join(text_outut_folder, text_output_file)
    
    with open(file_path, "w") as file:
        file.write(transcript)
    print("Audio successfullt trascribed. Transcript:")
    print(transcript)