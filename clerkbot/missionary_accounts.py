"""Create email reports of missionary balances.

"""
import sys

from io import StringIO

from clerkbot import gmail, configuration


EMAIL_BODY = '''Dear Missionary Family,

To help you keep track of mission expenses, I'm sending you a monthly balance 
summary. Your missionary's account currently has this much money in it:

{}

Please feel free to make an appointment with the bishop if you'd ever like to 
discuss financing your missionary.

For more details about how this all works, please read on.

Starting the month that your missionary enters the MTC, the church withdraws 
$400 from their account (around the 6th day of the month). Monthly 
withdrawals continue until there have been 18 or 24 of them (depending on time
of service). It works out that the last withdrawal will usually be during the 
month prior to the month in which your missionary comes home.

If your missionary has completed his or her service and has a positive balance,
we will sweep the remaining funds into the overall ward mission fund. For both
policy and legal reasons, excess funds cannot be refunded to donors.    

With regard to financing missionary service, the church handbook says:

    The primary responsibility to provide financial support for a missionary 
    lies with the individual and the family. Generally, missionaries should not 
    rely entirely on people outside of their family for financial support.

    Missionaries and their families should make appropriate sacrifices to 
    provide financial support for a mission. It is better for a person to delay 
    a mission for a time and earn money toward his or her support than to rely 
    entirely on others. However, worthy missionary candidates should not be 
    prevented from serving missions solely for financial reasons when they and 
    their families have sacrificed according to their capability.

Regards,
{} 
'''

NOTIFICATION_BODY = '''Hello,

Drafts for missionary account emails have been created for you. After reviewing
them for accuracy, feel free to send them.

--ClerkBot

'''


class Account:
    def __init__(self, name, balance):
        self.name = name
        self.balance = float(balance)

    @property
    def balance_str(self):
        return f'${self.balance:,.2f}'


class Tee:
    def __init__(self, files):
        self.files = files

    def write(self, s):
        for f in self.files:
            f.write(s)


def create_report_emails(s):
    assert s.logged_in, 'Expected logged in session.'

    config = configuration.read()
    report = s.get_ward_mission_report()
    accounts = process_lines(report)
    buffer = StringIO()
    tee = Tee([sys.stdout, buffer])
    for account in accounts:
        create_email(config, account, tee)
    notification = gmail.create_message(
        'me',
        config['emails'].get('mission_account_notifications'),
        'Mission account summaries ready',
        NOTIFICATION_BODY + buffer.getvalue()
    )
    gmail.send_message(notification)


def process_lines(report):
    items = []
    for line in report['lines']:
        if 'unitSubcategory' not in line['subcategory']:
            continue
        name = line['subcategory']['unitSubcategory']
        start = line['startBalance']
        income = line['income']
        expense = line['expense']
        transfers = line['transfers']
        balance = start + income + expense + transfers
        items.append(Account(name, balance))
    return items


def create_email(config, account, f):
    to = config['emails'].get(account.name)
    clerk_name = config['emails'].get('clerk_name', 'Ward Clerk')
    summary = f'{account.name} {account.balance_str}'
    if to:
        text = EMAIL_BODY.format(summary, clerk_name)
        message = gmail.create_message(
            'me',
            to,
            'Mission account - ' + account.name,
            text,)
        try:
            gmail.create_draft(message)
            print(summary, '— Email draft created to:', to, file=f)
        except Exception as e:
            print('Error creating email draft:', e, file=f)
    else:
        print(summary, '— No email configured', file=f)
