const getFormData = () => ({
    sender_email: document.getElementById('sender_email').value,
    sender_password: document.getElementById('sender_password').value,
    recipient: document.getElementById('to').value,
    subject: document.getElementById('subject').value,
    content: document.getElementById('body').value
});

const sendRequest = async (url, data) => {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return response.json();
    } catch (error) {
        alert('Error: ' + error.message);
    }
};

const updateEmailFields = (result) => {
    if (result.email_subject) document.getElementById('subject').value = result.email_subject;
    if (result.email_body) document.getElementById('body').value = result.email_body;
};

document.getElementById('email-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    const data = getFormData();
    const result = await sendRequest('/emails/send_email', data);
    alert(result.message || result.error);
});

document.getElementById('generate-email-btn').addEventListener('click', async function() {
    const data = getFormData();
    const result = await sendRequest('/emails/generate_email', data);
    if (result) updateEmailFields(result);
});

const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = 'en-US';
recognition.interimResults = false;

document.getElementById('voice-btn').addEventListener('click', () => {
    recognition.start();
    document.getElementById('body').placeholder = "Listening...";
});

recognition.onresult = async (event) => {
    const voiceText = event.results[0][0].transcript;
    document.getElementById('body').value = voiceText;
    
    const result = await sendRequest('/emails/generate_email', { content: voiceText });
    if (result) updateEmailFields(result);
};

recognition.onerror = (event) => {
    alert('Voice recognition error: ' + event.error);
    document.getElementById('body').placeholder = "Voice recognition failed.";
};

recognition.onend = () => {
    document.getElementById('body').placeholder = "Enter your email content...";
};