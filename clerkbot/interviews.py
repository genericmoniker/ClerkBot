import tempfile
from pathlib import Path
from clerkbot import gmail, configuration

EMAIL_BODY = '''Hello,

Please find attached the latest Action and Interview List.

Regards,
{}
'''


def create_list_email(s):
    assert s.logged_in, 'Expected logged in session.'
    config = configuration.read()
    pdf_data = s.get_action_interview_list()
    with tempfile.TemporaryDirectory() as temp_dir:
        attachment = Path(temp_dir) / 'Action and Interview List.pdf'
        attachment.write_bytes(pdf_data)
        to = config['emails'].get('interview_notifications')
        body = EMAIL_BODY.format(
            config['emails'].get('clerk_name', 'Ward Clerk')
        )
        notification = gmail.create_message(
            'me', to, 'Action and Interview List', body, [attachment]
        )
        gmail.send_message(notification)
        print('Email sent.')
