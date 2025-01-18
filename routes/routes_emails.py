from flask import Blueprint, request, jsonify
import os
import base64
import pickle
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.auth.transport.requests import Request

emails_routes = Blueprint('emails_routes', __name__)

# Define the scope for Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Function to get Gmail API credentials
def get_credentials():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

# Route to send email using Gmail API
@emails_routes.route('/send_email', methods=['POST'])
def send_email():
    data = request.get_json()
    
    # Fetch necessary data
    recipient = data.get('recipient')
    subject = data.get('subject')
    content = data.get('content')

    if not recipient or not subject or not content:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        creds = get_credentials()
        service = build('gmail', 'v1', credentials=creds)

        # Create email message
        message = MIMEMultipart()
        message['to'] = recipient
        message['subject'] = subject
        msg = MIMEText(content)
        message.attach(msg)

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

        # Send the email
        message = service.users().messages().send(userId='me', body={'raw': raw_message}).execute()
        return jsonify({"message": "Email sent successfully!"}), 200
    except HttpError as error:
        return jsonify({"error": f"An error occurred: {error}"}), 500