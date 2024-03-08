

from backend.audio_processing.record_audio import record_audio

def test_record_audio(filepath):
    record_audio(filepath) 


test_record_audio("audio.wav")