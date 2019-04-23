"""
Module for working with Gmail, including creating draft emails and sending
emails.

Gmail docs:
https://developers.google.com/gmail/api/guides/sending

This uses the new Python 3.6 email API. Docs are here:
https://docs.python.org/3/library/email.html#module-email
https://docs.python.org/3/library/email.examples.html 
"""
import base64
import mimetypes
from email.message import EmailMessage
from os import fspath
from pathlib import Path

import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client import tools

from oauth2client.file import Storage

from clerkbot.paths import CONF_DIR

CLIENT_SECRET_FILE = CONF_DIR / 'client_secret.json'
CREDENTIALS_FILE = CONF_DIR / 'clerkbot.json'

APPLICATION_NAME = 'ClerkBot'

# If modifying SCOPES, delete your previously saved CREDENTIALS_FILE.
SCOPES = 'https://www.googleapis.com/auth/gmail.compose'

# The documentation says to do this:
# flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
# But that interferes with my own command line parsing, so:
flags = {}


def create_message(sender, to, subject, message_text, attachments=None):
    """Create a message for an email.

    :param sender: Email address of the sender.
    :param to: Email address of the receiver (may be a comma-separated list).
    :param subject: The subject of the email message.
    :param message_text: The text of the email message.
    :param attachments: List of pathlib.Path of files to attach.
    :return: A dict containing a base64url encoded email object.
    """
    message = EmailMessage()
    message['To'] = to
    message['From'] = sender
    message['Subject'] = subject
    message.set_content(message_text)
    for path in attachments or []:
        add_attachment(message, path)
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}


def add_attachment(message, path):
    content_type, encoding = mimetypes.guess_type(fspath(path))
    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    maintype, subtype = content_type.split('/', 1)
    message.add_attachment(
        path.read_bytes(),
        maintype=maintype,
        subtype=subtype,
        filename=path.name,
    )


def create_draft(message: dict):
    """Create and insert a draft email.

    :param message: An email message, as created with `create_message`.
    :return: Draft object, including draft id and message meta data.
    :raise: googleapiclient.errors.HttpError on error.
    """
    service = get_service()
    message = {'message': message}
    draft = (
        service.users().drafts().create(userId='me', body=message).execute()
    )
    return draft


def send_message(message: dict):
    """Send an email message.

    :param message: An email message, as created with `create_message`.
    :return: Message object, including draft id and message meta data.
    :raise: googleapiclient.errors.HttpError on error.
    """
    service = get_service()
    sent = service.users().messages().send(userId='me', body=message).execute()
    return sent


def get_service():
    """Get an authenticated gmail service instance."""
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    return discovery.build('gmail', 'v1', http=http)


def get_credentials():
    """Get user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    :return: Credentials, the obtained credential.
    """
    store = Storage(fspath(CREDENTIALS_FILE))
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to', CREDENTIALS_FILE)
    return credentials
