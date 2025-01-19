document.getElementById('email-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const sender_email = document.getElementById('sender_email').value;
    const sender_password = document.getElementById('sender_password').value;
    const to = document.getElementById('to').value;
    const subject = document.getElementById('subject').value;
    const body = document.getElementById('body').value;

    const response = await fetch('/send_email', {
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