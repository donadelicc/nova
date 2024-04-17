from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify, send_from_directory

import os
import asyncio


from utils.transcribe_audio import transcribe_audio, detect_language, translate_transcription
from utils.response_handling import response_memory
from utils.text_to_speech import text_to_speech
    
app = Flask(__name__)

@app.route('/')
def index():
    
    ## Lytte etter talekommandoer (javascript)
    
    return render_template('index.html')
    
@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    if 'audioFile' not in request.files:
        return jsonify({'message': 'Ingen fil del av forespørselen'}), 400
    file = request.files['audioFile']
    if file.filename == '':
        return jsonify({'message': 'Ingen fil valgt for opplasting'}), 400
    if file:
        filename = file.filename
        # save_path = os.path.join(os.getenv('AUDIO_INPUT_FOLDER'), filename)
        save_path = os.getenv('AUDIO_INPUT_FOLDER') + "/" + filename
        file.save(save_path)
        
        # Prosessér den opplastede filen umiddelbart etter lagring
        asyncio.run(process_query(filename))  # Oppdatert for å sende filbanen som argument

        return jsonify({'message': 'Fil lastet opp og prosessert suksessfullt'}), 200
    
@app.route('/get_response_audio')
def get_response_audio():
    audio_output_folder = os.getenv("AUDIO_OUTPUT_FOLDER")
    return send_from_directory(directory=audio_output_folder, path="audio.mp3", as_attachment=True)


async def process_query(audio_input_file):
    print("Audio Input Folder:", os.getenv("AUDIO_INPUT_FOLDER"))
    print("Text Output Folder:", os.getenv("TEXT_OUTPUT_FOLDER"))

    text_file = "Q.txt"
    await transcribe_audio(audio_input_file, text_file)
    transcription_lang = await detect_language(text_file)
    if transcription_lang != "no":
       await translate_transcription(text_file)
    res = await response_memory(text_file)
    audio_output_file = "audio.mp3"
    await text_to_speech(res, audio_output_file)
    # Legg til logikk her hvis du vil returnere den prosesserte filen eller resultatet til klienten

if __name__ == '__main__':
    app.run(debug=True)