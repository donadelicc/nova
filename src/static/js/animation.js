const activationWaiting = document.querySelector('.start');
const wakeWord = document.querySelector('.vekkeord').parentNode;
const questionWaiting = document.querySelector('.image-ear').parentNode;
const askQuestion = document.querySelector('.spørsmål').parentNode;
const processing = document.querySelector('.image-process').parentNode;
const speaking = document.querySelector('.image-speak').parentNode;

function hideAllStates() {
    activationWaiting.style.opacity = '0';
    wakeWord.style.opacity = '0';
    questionWaiting.style.opacity = '0';
    askQuestion.style.opacity = '0';
    processing.style.opacity = '0';
    speaking.style.opacity = '0';
}

export function updateUI(state) {
    hideAllStates();
    console.log("UI state: " +state);
    switch(state) {
        case 'activate':
            activationWaiting.style.opacity = '1';
            wakeWord.style.opacity = '1';
            break;
        case 'listening':
            questionWaiting.style.opacity = '1';
            askQuestion.style.opacity = '1';
            break;
        case 'processing':
            processing.style.opacity = '1';
            break;
        case 'speaking':
            speaking.style.opacity = '1';
            break;
    }
}