import speech_recognition as sr
import pyttsx3
import os
import sys

# Antar at du har implementert følgende funksjoner i dine backend-moduler
from transcribe_audio import transcribe_audio, detect_language, translate_transcription
from response_handling import response_memory
from text_to_speech import text_to_speech, play_audio_file


def listen_and_respond():
    recognizer = sr.Recognizer()
    
    while True:
        try:
            with sr.Microphone() as mic:
                print("Adjusting for ambient noise, please wait...")
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                print("Say 'alexa' to activate...")
                audio = recognizer.listen(mic)

                text = recognizer.recognize_google(audio)
                text = text.lower()
                if text == "alexa":
                    print("Activated. Please ask your question.")
                    while True:
                        try:
                            audio = recognizer.listen(mic, timeout=10)
                            text = recognizer.recognize_google(audio)
                            text = text.lower()
                            if text == "stop alexa":
                                print("Deactivated.")
                                sys.exit()
                            else:
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
                                # audio_output_path = os.path.join(audio_output_folder, audio_output_file)
                                audio_output_path = audio_output_folder+"/"+audio_output_file
                                play_audio_file(audio_output_path)
                                print("Please ask your question or say 'stop alexa' to deactivate.")
                    
                        except sr.WaitTimeoutError:
                            print("No question detected. Say 'alexa' to activate again.")
                            break
                
                    
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

if __name__ == '__main__':
    while True:
        listen_and_respond()
