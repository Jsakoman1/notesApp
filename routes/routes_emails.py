from flask import Blueprint, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

emails_routes = Blueprint('emails_routes', __name__)

# Route to send email using Titan Mail SMTP
@emails_routes.route('/send_email', methods=['POST'])
def send_email():
    data = request.get_json()

    # Fetch necessary data
    sender_email = data.get('sender_email')  # Titan Mail email
    sender_password = data.get('sender_password')  # Titan Mail password
    recipient_email = data.get('recipient')  # Recipient's email
    subject = data.get('subject')  # Email subject
    content = data.get('content')  # Email body

    # Validate input
    if not all([sender_email, sender_password, recipient_email, subject, content]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Titan Mail SMTP configuration
        smtp_server = "smtp.titan.email"
        smtp_port = 587  # For TLS

        # Create email message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient_email
        message["Subject"] = subject
        message.attach(MIMEText(content, "plain"))

        # Send email using Titan Mail SMTP
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Enable TLS encryption
            server.login(sender_email, sender_password)
            server.send_message(message)

        return jsonify({"message": "Email sent successfully!"}), 200

    except smtplib.SMTPException as error:
        return jsonify({"error": f"Failed to send email: {str(error)}"}), 500