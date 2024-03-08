import speech_recognition as sr
import pyttsx3
import os

# Antar at du har implementert følgende funksjoner i dine backend-moduler
from backend.transcribe_audio import transcribe_audio
from backend.response_handling import response, response_memory
from backend.text_to_speech import text_to_speech, play_audio_file


def listen_and_respond():
    
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Adjusting for ambient noise, please wait...")
        recognizer.adjust_for_ambient_noise(source, duration=0.2)
        print("Say 'alexa' to activate...")
        audio = recognizer.listen(source)
        audio.energy_threshold = 4000
        try:
            transcription = recognizer.recognize_google(audio)
            if transcription.lower() == "alexa":
                lytter = True
                while lytter:
                    if transcription.lower() == "stop alexa":
                        lytter = False
                    print("Activated. Please ask your question.")
                    audio_input_folder = "audio_input"
                    audio_input_file = "audio.wav"
                    audio_input = os.path.join(audio_input_folder, audio_input_file)
                    audio = recognizer.listen(source)
                    source.pause_threshold = 1
                    with open(audio_input, "wb") as f:
                        f.write(audio.get_wav_data())

                    text_file = "transcript.txt"
                    audio_output_folder = "audio_output"
                    audio_output_file = "audio.mp3"
                    transcribe_audio(audio_input_file, text_file)
                    
                    res = response_memory(text_file)
                    text_to_speech(res, audio_output_file)
                    audio = os.path.join(audio_output_folder, audio_output_file)
                    play_audio_file(audio)
                    

                    
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

if __name__ == '__main__':
    while True:
        listen_and_respond()
