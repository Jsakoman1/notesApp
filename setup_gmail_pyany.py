from flask import Flask, redirect, request
import google_auth_oauthlib.flow

app = Flask(__name__)

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

@app.route('/authorize')
def authorize():
    """Redirect to Google's OAuth 2.0 authorization page."""
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'credentials.json', SCOPES)
    flow.redirect_uri = 'http://www.sakoman.ch/authorized'  # Set your PythonAnywhere URL here
    authorization_url, state = flow.authorization_url(
        access_type='offline', include_granted_scopes='true')
    return redirect(authorization_url)

@app.route('/authorized')
def authorized():
    """Handle the OAuth callback and save the token."""
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'credentials.json', SCOPES)
    flow.redirect_uri = 'http://www.sakoman.ch/authorized'  # Same URL as before
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    # Save credentials to token.json
    with open('token.json', 'w') as token:
        token.write(credentials.to_json())
    return 'Authorization complete! Token saved.'

if __name__ == '__main__':
    app.run(debug=True)