from flask import Blueprint, request, jsonify, current_app as app
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import openai
import whisper

emails_routes = Blueprint('emails_routes', __name__)
client = openai.OpenAI()

# Helper function to generate email content
def generate_email_content(content, role):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are an assistant helping to generate {role}."},
                {"role": "user", "content": content}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        app.logger.error(f"Error generating {role}: {e}")
        return None

# Helper function to send email
def send_smtp_email(sender_email, sender_password, recipient_email, subject, content):
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
        return {"message": "Email sent successfully!"}
    except smtplib.SMTPException as error:
        app.logger.error(f"Error while sending email: {error}")
        return {"error": f"Failed to send email: {str(error)}"}

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

    response = send_smtp_email(sender_email, sender_password, recipient_email, subject, content)
    return jsonify(response), 200 if 'message' in response else 500

# Route for testing SMTP connection
@emails_routes.route('/test_email')
def test_email():
    try:
        server = smtplib.SMTP("smtp.titan.email", 587)
        server.starttls()
        server.quit()
        return "Successfully connected to TitanMail SMTP server."
    except Exception as e:
        return f"Failed to connect: {e}"

# Route to generate email using OpenAI
@emails_routes.route('/generate_email', methods=['POST'])
def generate_email():
    data = request.get_json()
    content = data.get('content')

    if not content:
        return jsonify({"error": "Content is required"}), 400

    email_body = generate_email_content(f"Write an email in a natural tone with the following content: {content}", "email body")
    if not email_body:
        return jsonify({"error": "Failed to generate email body"}), 500

    email_subject = generate_email_content(f"Generate a suitable subject for the following email body: {email_body}", "email subject")
    if not email_subject:
        return jsonify({"error": "Failed to generate email subject"}), 500

    return jsonify({"email_subject": email_subject, "email_body": email_body}), 200

# Route to process audio and generate email
@emails_routes.route('/process_audio', methods=['POST'])
def process_audio():
    try:
        # Save the uploaded file
        audio_file = request.files['audio']
        file_path = f"/tmp/{audio_file.filename}"
        audio_file.save(file_path)

        # Transcribe the audio using Whisper
        model = whisper.load_model("base")  # Choose the desired model size
        result = model.transcribe(file_path)
        text = result['text']

        # Generate email using the transcribed text
        response = generate_email_from_text(text)

        return jsonify(response), 200

    except Exception as e:
        app.logger.error(f"Error processing audio: {e}")
        return jsonify({"error": f"Failed to process audio: {e}"}), 500

# Function to generate email from text
def generate_email_from_text(content):
    email_body = generate_email_content(f"Write an email in a natural tone with the following content: {content}", "email body")
    if not email_body:
        return {"error": "Failed to generate email body"}

    email_subject = generate_email_content(f"Generate a suitable subject for the following email body: {email_body}", "email subject")
    if not email_subject:
        return {"error": "Failed to generate email subject"}

    return {"email_subject": email_subject, "email_body": email_body}