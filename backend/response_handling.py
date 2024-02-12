import os
from openai import OpenAI
import pyttsx3

audio_input_folder = "audio_input"
text_output_folder = "text_input"
audio_output_folder = "static/audio_output"

if not os.path.exists(text_output_folder):
    os.makedirs(text_output_folder)
if not os.path.exists(audio_output_folder):
    os.makedirs(audio_output_folder)

def response(file_name):

    file_path = os.path.join(text_output_folder, file_name)
    
    with open(file_path, "r") as file:
        question = file.read()

    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Du er en talestyrt assistent som etter beste evne prøver å besvare spørsmål som du blir stilt."},
            {"role": "user", "content": f"{question}"}
        ],
        temperature=0.1,
        max_tokens=150
        
    )
    
    output = response.choices[0].message.content
    print("----------------------------")
    print("GPT-3 response:")
    print(output)
    return output

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


engine = pyttsx3.init()

def speak_text(text):
    engine.say(text)
    engine.runAndWait()
    
