document.getElementById('email-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const sender_email = document.getElementById('sender_email').value;
    const sender_password = document.getElementById('sender_password').value;
    const to = document.getElementById('to').value;
    const subject = document.getElementById('subject').value;
    const body = document.getElementById('body').value;

    const response = await fetch('/emails/send_email', {  // Updated to include '/emails'
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            sender_email,
            sender_password,
            recipient: to,
            subject,
            content: body
        })
    });

    const result = await response.json();
    alert(result.message || result.error);
});

document.getElementById('generate-email-btn').addEventListener('click', async function() {
    const sender_email = document.getElementById('sender_email').value;
    const sender_password = document.getElementById('sender_password').value;
    const to = document.getElementById('to').value;
    const subject = document.getElementById('subject').value;
    const body = document.getElementById('body').value; // Get the body content

    // Include body content in emailData for generation
    const emailData = {
        sender_email,
        sender_password,
        recipient: to,
        subject,
        content: body  // Pass the body content here
    };

    try {
        const response = await fetch('/emails/generate_email', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(emailData)  // Send the emailData including content
        });

        const result = await response.json();

        if (response.ok) {
            if (result.email_subject) {
                document.getElementById('subject').value = result.email_subject;  // Populate the subject with generated subject
            }
            if (result.email_body) {
                document.getElementById('body').value = result.email_body;  // Populate the body with generated content
            }
        } else {
            alert(result.error || 'Error generating email content');
        }
    } catch (error) {
        alert('Error generating email: ' + error.message);
    }
});

// Voice recognition
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

    // Optionally auto-generate the email
    try {
        const response = await fetch('/emails/generate_email', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ content: voiceText }) // Send the transcribed text
        });

        const result = await response.json();

        if (response.ok) {
            if (result.email_subject) {
                document.getElementById('subject').value = result.email_subject;
            }
            if (result.email_body) {
                document.getElementById('body').value = result.email_body;
            }
        } else {
            alert(result.error || 'Error generating email content');
        }
    } catch (error) {
        alert('Error generating email: ' + error.message);
    }
};

recognition.onerror = (event) => {
    alert('Voice recognition error: ' + event.error);
    document.getElementById('body').placeholder = "Voice recognition failed.";
};

recognition.onend = () => {
    document.getElementById('body').placeholder = "Enter your email content...";
};