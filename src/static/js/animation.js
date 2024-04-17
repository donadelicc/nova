const activationWaiting = document.querySelector('.start');
const questionWaiting = document.querySelector('.image-ear').parentNode;
const processing = document.querySelector('.image-process').parentNode;
const speaking = document.querySelector('.image-speak').parentNode;

function hideAllStates() {
    activationWaiting.style.opacity = '0';
    questionWaiting.style.opacity = '0';
    processing.style.opacity = '0';
    speaking.style.opacity = '0';
}

export function updateUI(state) {
    hideAllStates();
    switch(state) {
        case 'waitingForActivation':
            activationWaiting.style.opacity = '1';
            break;
        case 'waitingForQuestion':
            questionWaiting.style.opacity = '1';
            break;
        case 'processing':
            processing.style.opacity = '1';
            break;
        case 'speaking':
            speaking.style.opacity = '1';
            break;
    }
}


