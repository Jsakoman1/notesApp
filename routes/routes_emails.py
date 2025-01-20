# routes/routes_emails.py
from flask import Blueprint, request, jsonify, current_app as app
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import openai

emails_routes = Blueprint('emails_routes', __name__)
client = openai.OpenAI()

# Route to send email using Titan Mail SMTP
@emails_routes.route('/send_email', methods=['POST'])
def send_email():
    data = request.get_json()

    sender_email = data.get('sender_email')
    sender_password = data.get('sender_password')
    recipient_email = data.get('recipient')
    subject = data.get('subject')
    content = data.get('content')

    if not all([sender_email, sender_password, recipient_email, subject, content]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        smtp_server = "smtp.titan.email"
        smtp_port = 587

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient_email
        message["Subject"] = subject
        message.attach(MIMEText(content, "plain"))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)

        return jsonify({"message": "Email sent successfully!"}), 200

    except smtplib.SMTPException as error:
        app.logger.error(f"Error while sending email: {error}")
        return jsonify({"error": f"Failed to send email: {str(error)}"}), 500

# Corrected route for testing the SMTP connection
@emails_routes.route('/test_email')
def test_email():
    try:
        server = smtplib.SMTP("smtp.titan.email", 587)
        server.starttls()
        server.quit()
        return "Successfully connected to TitanMail SMTP server."
    except Exception as e:
        return f"Failed to connect: {e}"
    
@emails_routes.route('/generate_email', methods=['POST'])
def generate_email():
    data = request.get_json()
    content = data.get('content')  # Expecting the content field from the JS request

    if not content:
        return jsonify({"error": "Content is required"}), 400

    try:
        # Step 1: Generate the body content of the email using OpenAI
        response_body = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant helping to generate email body text."},
                {"role": "user", "content": f"Write an email in a natural tone with the following content: {content} (Do not add 'Body:' prefix, just the email content)"}
            ]
        )

        email_body = response_body.choices[0].message.content.strip()

        # Step 2: Use the generated body to create the subject (without adding 'Subject:' prefix)
        response_subject = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant helping to generate email subjects."},
                {"role": "user", "content": f"Generate a suitable subject for the following email body: {email_body} (Do not add 'Subject:' prefix, just the subject text)"}
            ]
        )

        email_subject = response_subject.choices[0].message.content.strip()

        return jsonify({"email_subject": email_subject, "email_body": email_body}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@emails_routes.route('/process_audio', methods=['POST'])
def process_audio():
    try:
        # Save the uploaded file
        audio_file = request.files['audio']
        file_path = f"/tmp/{audio_file.filename}"
        audio_file.save(file_path)

        # Transcribe the audio using Whisper
        import whisper
        model = whisper.load_model("base")  # Choose the desired model size
        result = model.transcribe(file_path)
        text = result['text']

        # Generate email using the transcribed text
        response = generate_email_from_text(text)

        return jsonify(response), 200

    except Exception as e:
        app.logger.error(f"Error processing audio: {e}")
        return jsonify({"error": f"Failed to process audio: {e}"}), 500
    

def generate_email_from_text(content):
    try:
        # Step 1: Generate the email body using OpenAI
        response_body = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant helping to generate email body text."},
                {"role": "user", "content": f"Write an email in a natural tone with the following content: {content}"}
            ]
        )
        email_body = response_body.choices[0].message.content.strip()

        # Step 2: Generate the email subject using OpenAI
        response_subject = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant helping to generate email subjects."},
                {"role": "user", "content": f"Generate a suitable subject for the following email body: {email_body}"}
            ]
        )
        email_subject = response_subject.choices[0].message.content.strip()

        return {"email_subject": email_subject, "email_body": email_body}
    except Exception as e:
        raise ValueError(f"Failed to generate email: {e}")