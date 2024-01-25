from flask import Flask, render_template, request, redirect, url_for, session
from backend.audio_processing import record_audio, transcribe_audio
from backend.response_handling import response

app = Flask(__name__)
app.secret_key = 'preben sin nøkkel'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'record' in request.form:

            audio_file = "audio.wav"
            text_file = "transcript.txt"
            record_audio(audio_file)
            transcribe_audio(audio_file, text_file)
            res = response(text_file)
            session['response'] = res

        return redirect(url_for('index'))

    return render_template('index.html', response=session.get('response'))

if __name__ == '__main__':
    app.run(debug=True)
