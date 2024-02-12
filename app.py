from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime


from backend.audio_processing import record_audio
from backend.transcribe_audio import transcribe_audio
from backend.response_handling import response, text_to_speech

app = Flask(__name__)
app.secret_key = 'preben sin nøkkel'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'record' in request.form:

            audio_input_file = "audio.wav"
            text_file = "transcript.txt"
            audio_output_file = "audio.mp3"
            
            record_audio(audio_input_file)
            transcribe_audio(audio_input_file, text_file)
            res = response(text_file)
            session['response'] = res
            text_to_speech(res, audio_output_file)
            
        return redirect(url_for('index'))

    now = datetime.now().timestamp()  # Generer et unikt tidsstempel til
    return render_template('index.html', response=session.get('response'), now=now)

if __name__ == '__main__':
    app.run(debug=True)
