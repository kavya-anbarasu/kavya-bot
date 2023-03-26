from __future__ import print_function

import base64
import os.path

# from email.message import 
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def get_credentials():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def gmail_send_message(
        email_subject, email_body, email_to, email_from="kavya_bot@mit.edu"):
    '''
    Create and send an email message
    Print the returned  message id
    Returns: Message object, including message id
    '''
    creds = get_credentials()
    try:
        service = build('gmail', 'v1', credentials=creds)
        message = MIMEText(email_body, 'html')

        # message.set_content(email_body)

        message['To'] = email_to
        message['From'] = email_from
        message['Subject'] = email_subject

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {
            'raw': encoded_message
        }

        send_message = (service.users().messages().send
                        (userId="me", body=create_message).execute())
        # print(F'Message Id: {send_message["id"]}')
    except HttpError as error:
        print(F'An error occurred: {error}')
        send_message = None

    return send_message


if __name__ == '__main__':
    gmail_send_message(
        "testing bot send with new lines",
        "boop boop beep.\nkavya bot is gaining sentience.\nbeep beep.",
        "kavyaa@mit.edu"
    )
