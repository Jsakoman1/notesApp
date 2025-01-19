from flask import Blueprint, request, jsonify, current_app as app
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

emails_routes = Blueprint('emails_routes', __name__)

# Route to send email using SMTP
@emails_routes.route('/send_email', methods=['POST'])
def send_email():
    data = request.get_json()

    # Fetch necessary data from the request
    sender_email = data.get('sender_email')  # Sender's email
    sender_password = data.get('sender_password')  # Sender's password
    recipient_email = data.get('recipient')  # Recipient's email
    subject = data.get('subject')  # Email subject
    content = data.get('content')  # Email body

    # Validate input
    if not all([sender_email, sender_password, recipient_email, subject, content]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Use PythonAnywhere's SMTP server (or another SMTP service like Gmail)
        smtp_server = "smtp.pythonanywhere.com"  # For PythonAnywhere, use their SMTP server
        smtp_port = 587  # Port for TLS

        # Create email message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient_email
        message["Subject"] = subject
        message.attach(MIMEText(content, "plain"))

        # Send email using the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Enable TLS encryption
            server.login(sender_email, sender_password)
            server.send_message(message)

        return jsonify({"message": "Email sent successfully!"}), 200

    except smtplib.SMTPException as error:
        # Log the error to help debug
        app.logger.error(f"Error while sending email: {error}")
        return jsonify({"error": f"Failed to send email: {str(error)}"}), 500