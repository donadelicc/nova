import os
from openai import OpenAI

audio_input_folder = os.getenv("AUDIO_INPUT_FOLDER")
audio_output_folder = os.getenv("AUDIO_OUTPUT_FOLDER")

if not os.path.exists(audio_output_folder):
    os.makedirs(audio_output_folder)
if not os.path.exists(audio_input_folder):
    os.makedirs(audio_input_folder)
    


def text_to_speech(answer, filename):
    client = OpenAI()
    file_path = os.path.join(audio_output_folder, filename)
    response = client.audio.speech.create(
    model="tts-1",
    voice="onyx",
    input=answer
    )
    
    with open(file_path, "wb") as file:
        file.write(response.content)
    print("Audio file successfully created.")


from playsound import playsound

def play_audio_file(file_path):
    try:
        playsound(file_path)
        print("Playing audio file:", file_path)
    except Exception as e:
        print("Error playing audio file:", e)