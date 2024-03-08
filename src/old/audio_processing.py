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
record_seconds = 3  # Record duration

audio_input_folder = "audio_input"
text_output_folder = "text_input"
audio_output_folder = "audio_output"

if not os.path.exists(audio_input_folder):
    os.makedirs(audio_input_folder)
if not os.path.exists(text_output_folder):
    os.makedirs(text_output_folder)
    

def record_audio(file_name, folder):
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

    file_path = os.path.join(folder, file_name)

    # Lagrer opptaket til en fil
    wf = wave.open(file_path, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    return file_path

