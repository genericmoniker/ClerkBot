import io
from contextlib import contextmanager
from datetime import datetime, timedelta

from lcr import API

from clerkbot import gmail, configuration
from clerkbot.paths import CONF_DIR


def create_notification(lcr: API):
    buffer = io.StringIO()
    with last_checked() as checked_date:
        # We don't include records moved today because if they move after the
        # script ran for today, we'd skip those tomorrow and miss them.
        _generate_body(lcr, buffer, checked_date, datetime.today().date())
    body = buffer.getvalue()
    buffer.close()
    if body:
        print('Sending email notification.')
        print(body)
        _send_email(body)
    else:
        print('No new record changes.')


def _generate_body(lcr, buffer, since, until):
    """Generate the notification email body.

    :param s: lds_session instance.
    :param buffer: buffer into which to write the body.
    :param since: include records moved on or after this date.
    :param until: include records moved before this date.
    """
    moved_in = _get_members_moved(lcr.members_moved_in(1), since, until)
    if moved_in:
        print('These records have been moved into the ward:', file=buffer)
        for mi in moved_in:
            prior = mi['priorUnitName']
            prior = f'from the {prior}' if prior else 'from an unknown unit'
            print('-', mi['name'], prior, file=buffer)
        print(file=buffer)

    moved_out = _get_members_moved(lcr.members_moved_out(1), since, until)
    if moved_out:
        print('These records have been moved out of the ward:', file=buffer)
        for mo in moved_out:
            next = mo['nextUnitName']
            next = f'to the {next}' if next else 'to an unknown unit'
            if mo['addressUnknown'] is True:
                next += ' (address unknown)'
            print('-', mo['name'], 'to the', next, file=buffer)


def _get_members_moved(members, since, until):
    """Get members with move dates on or after `since`, and before `until`."""
    if since >= until:
        raise ValueError('Invalid since (%s) and until (%s)', since, until)
    return [m for m in members if until > _get_move_date(m) >= since]


def _get_move_date(member):
    """Get the move date from a member moved in/out record."""
    # We want a date of the form '2019-07-21'. For members moved in, that is
    # currently 'moveDateCalc', and for members moved out, 'moveDate'.
    date_str = member.get('moveDateCalc', member.get('moveDate'))
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def _send_email(body):
    config = configuration.read()

    to = config['emails'].get('record_notifications')
    if to:
        message = gmail.create_message('me', to, 'Record notification', body)
        try:
            gmail.send_message(message)
            print('Email sent to:', to)
        except Exception as e:
            print('Error sending email:', e)
    else:
        print('No email configured for', 'record_notification')


@contextmanager
def last_checked():
    file = CONF_DIR / 'records-checked.txt'
    try:
        date_str = file.read_text().strip()
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except Exception as e:
        print('Reporting last 30 days because', e)
        date = (datetime.now() - timedelta(days=30)).date()

    yield date

    file.write_text(datetime.now().date().isoformat())
