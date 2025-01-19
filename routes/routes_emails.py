# routes/routes_emails.py
from flask import Blueprint, request, jsonify, current_app as app
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

emails_routes = Blueprint('emails_routes', __name__)

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