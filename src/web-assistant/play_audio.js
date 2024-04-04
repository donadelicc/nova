function playAudio(audioFilePath) {
    const audio = new Audio(audioFilePath);
    audio.play();
  }
  
  // Example usage (assuming you've generated the audio file)
  const generatedAudioFilePath = 'path/to/your/audio.mp3'; 
  playAudio(generatedAudioFilePath);

  