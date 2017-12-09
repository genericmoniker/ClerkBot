import argparse
import base64
from email.mime.text import MIMEText
from pathlib import Path

import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client import tools

from oauth2client.file import Storage

from clerk.paths import CONF_DIR

CLIENT_SECRET_FILE = CONF_DIR / 'client_secret.json'
APPLICATION_NAME = 'Clerk Tools'

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/clerk-tools.json
SCOPES = 'https://www.googleapis.com/auth/gmail.compose'

# The documentation says to do this:
# flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
# But that interferes with my own command line parsing, so:
flags = {}


def create_message(sender, to, subject, message_text):
    """Create a message for an email.

    :param sender: Email address of the sender.
    :param to: Email address of the receiver.
    :param subject: The subject of the email message.
    :param message_text: The text of the email message.
    :return: An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}


def create_draft(message_body):
    """Create and insert a draft email.

    :param message_body: The body of the email message, including headers.
    :return: Draft object, including draft id and message meta data.
    :raise: googleapiclient.errors.HttpError on error.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    message = {'message': message_body}
    draft = service.users().drafts().create(userId='me',
                                            body=message).execute()
    return draft


def get_credentials():
    """Get user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Return:
        Credentials, the obtained credential.
    """
    home_dir = Path.home()
    credential_dir = home_dir / '.credentials'
    credential_dir.mkdir(parents=True, exist_ok=True)
    credential_path = credential_dir / 'clerk-tools.json'

    store = Storage(str(credential_path))
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to', credential_path)
    return credentials
