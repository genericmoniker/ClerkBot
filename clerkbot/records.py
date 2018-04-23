import io
from contextlib import contextmanager
from datetime import datetime, timedelta

from clerkbot import gmail, configuration


def create_notification(s):
    buffer = io.StringIO()
    # TODO: real last_checked
    last_checked = (datetime.now() - timedelta(days=30)).date()
    _generate_body(s, buffer, last_checked)
    body = buffer.getvalue()
    buffer.close()
    if body:
        print('Sending email notification.')
        print(body)
        _send_email(body)
    else:
        print('No new record changes.')


def _generate_body(s, buffer, since):
    moved_in = [m for m in s.get_members_moved_in() if
                _parse_date(m['moveDate']) > since]
    if moved_in:
        print('These records have been moved into the ward:', file=buffer)
        for mi in moved_in:
            print(
                '-', mi['name'],
                'from the', mi['priorUnitName'],
                file=buffer
            )
        print(file=buffer)

    moved_out = [m for m in s.get_members_moved_out() if
                 _parse_date(m['moveDate']) > since]
    if moved_out:
        print('These records have been moved out of the ward:', file=buffer)
        for mo in moved_out:
            print(
                '-', mo['name'],
                'to the', mo['nextUnitName'],
                file=buffer
            )


def _parse_date(date_str):
    return datetime.strptime(date_str, "%Y%m%d").date()


def _send_email(body):
    config = configuration.read()

    to = config['emails'].get('record_notifications')
    if to:
        message = gmail.create_message(
            'me',
            to,
            'Record notification',
            body,
        )
        try:
            gmail.send_message(message)
            print('Email sent to:', to)
        except Exception as e:
            print('Error sending email:', e)
    else:
        print('No email configured for', 'record_notification')


@contextmanager
def last_checked():
    pass
