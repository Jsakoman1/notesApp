import os
import pickle
import base64
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.auth.transport.requests import Request

# If modifying the SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Path to the credentials.json file
CREDENTIALS_FILE = 'credentials.json'  # Place this file in your root directory

def authenticate_gmail():
    """Authenticate with Gmail API and return the service object"""
    creds = None
    # The token.json file stores the user's access and refresh tokens and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        with open('token.json', 'r') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.json', 'wb') as token:
            pickle.dump(creds, token)

    try:
        # Build the service object
        service = build('gmail', 'v1', credentials=creds)
        return service
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

def send_email(service, to, subject, body):
    """Send an email using the Gmail API"""
    try:
        # Create the message
        message = MIMEMultipart()
        message['to'] = to
        message['subject'] = subject
        msg = MIMEText(body)
        message.attach(msg)

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        # Send the email
        send_message = service.users().messages().send(userId='me', body={'raw': raw_message}).execute()
        print(f'Message sent: {send_message["id"]}')
        return send_message
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

def main():
    # Authenticate and get the Gmail service
    service = authenticate_gmail()

    if service:
        # Send email
        to = 'recipient@example.com'  # Replace with recipient's email
        subject = 'Test Email Subject'
        body = 'This is a test email sent from the Gmail API.'
        send_email(service, to, subject, body)
    else:
        print('Failed to authenticate with Gmail API.')

if __name__ == '__main__':
    main()