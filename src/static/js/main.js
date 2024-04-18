import { updateUI } from './animation.js';


const NAME = 'nova';

let isRecording = false; //  recording state
let audioChunks = [];
let mediaRecorder;



document.addEventListener('DOMContentLoaded', function() {
    updateUI('activate')
});

function startAssistant() {

    updateUI('activate')

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognizer = new SpeechRecognition();

    recognizer.start();
    recognizer.continuous = true;
    recognizer.interimResults = true;

    recognizer.onstart = () => {
        console.log("Adjusting for ambient noise, please wait...");
    };

    recognizer.onresult = async (event) => {

        const transcript = Array.from(event.results)
            .map(result => result[0].transcript)
            .join('');
    
        if (transcript.toLowerCase().includes(NAME) && !isRecording) {
            console.log("Activated. Please ask your question.");
            updateUI('listening');
            isRecording = true;
            recognizer.stop(); // Stop speech recognition to avoid conflict with MediaRecorder
            await startRecording();
           
        } else if (transcript.toLowerCase().includes("stop nova") && isRecording) {
            console.log("Deactivated.");
            await stopRecording();
            return
        }
    
        console.log("Voice detected. Processing...");
    };
    
    recognizer.onerror = (event) => {
        console.error("Error occurred:", event.error);
    };

}


async function startRecording() {

    console.log("startRecording() called")

    try {

        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];

        mediaRecorder.ondataavailable = event => {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = async () => {
            updateUI('processing');
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            const audioUrl = URL.createObjectURL(audioBlob);
            const formData = new FormData();
            formData.append("audioFile", audioBlob, "recording.wav");
            
            try {
                let uploadResponse = await fetch('/upload_audio', {
                    method: 'POST',
                    body: formData,
                });
                if (uploadResponse.ok) {
                    console.log("File sent to the server.");
                    fetchGeneratedAudio(); // Fetch and play the generated audio from the server
                    console.log("fetchGeneratedAudio() called")
                } else {
                    console.error("Server error during file upload.");
                }
            } catch (error) {
                console.error("Error sending file to the server:", error);
            } finally {
                restartSpeechRecognition();
            }

        };

        mediaRecorder.start();
        console.log("Recording started.");
        checkSilence();

    } catch {
        console.error("Error accessing media device:", error);
    
    }
}


function checkSilence() {
    const audioContext = new AudioContext();
    const source = audioContext.createMediaStreamSource(mediaRecorder.stream);
    const analyser = audioContext.createAnalyser();
    analyser.fftSize = 2048;

    source.connect(analyser);

    const buffer = new Float32Array(analyser.fftSize);
    const threshold = 0.1; // Adjust as needed
    let silenceDuration = 0; // In milliseconds
    const maxSilenceDuration = 2000; // Max silence before stopping

    setInterval(() => {
        analyser.getFloatTimeDomainData(buffer);

        const isSilent = buffer.every(sample => Math.abs(sample) < threshold);

        if (isSilent) {
            silenceDuration += 100; // Interval runs every 100ms
            if (silenceDuration >= maxSilenceDuration) {
                stopRecording();

            }
        } else {
            silenceDuration = 0;
        }
    }, 100); // Check every 100ms
}


async function stopRecording() {

    if (mediaRecorder && mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
        console.log("Recording stopped.");
    }
}

async function fetchGeneratedAudio() {

    try {
        const response = await fetch('/get_response_audio');
        if (response.ok) {
            const audioBlob = await response.blob();
            const audioUrl = URL.createObjectURL(audioBlob);
            const audio = new Audio(audioUrl);
   
            audio.play();
            updateUI('speaking');
            audio.onended = () => {
                // Gjenstart talegjenkjenning når lyden er ferdig spilt
                restartSpeechRecognition();
            };

            console.log("Playing generated audio.");
        } else {
            console.error("Error fetching the generated audio.");
        }
    } catch (error) {
        console.error("Could not fetch the generated audio file:", error);
    }
}


function restartSpeechRecognition() {
    console.log("restartSpeechRecognition() called");
    isRecording = false;
    startAssistant()
}

restartSpeechRecognition()
