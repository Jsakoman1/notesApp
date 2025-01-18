document.getElementById('email-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const to = document.getElementById('to').value;
    const subject = document.getElementById('subject').value;
    const body = document.getElementById('body').value;

    const response = await fetch('/send_email', {  // Update this line to match the Flask route
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ recipient: to, subject: subject, content: body })  // Use proper JSON keys
    });

    const result = await response.json();
    alert(result.message || result.error);
});