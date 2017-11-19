"""Create email reports of missionary balances.

"""
import configparser
from datetime import datetime

from clerk import lds_session, gmail
from clerk.paths import CONF_DIR


EMAIL_BODY = '''Dear Missionary Family,

To make it easier for you to keep track of mission expenses, I'm sending you a 
monthly summary. The ward mission category balance for your missionary is 
currently:

{}

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

If your missionary has completed his or her service and has a positive balance,
we will sweep the remaining funds into the overall ward mission fund. For both
policy and legal reasons, excess funds cannot be refunded to donors.    

Please feel free to make an appointment with the bishop if you'd ever like to 
discuss challenges financing your missionary.

Regards,
{} 
'''


class Account:
    def __init__(self, name, balance):
        self.name = name
        self.balance = float(balance)

    @property
    def balance_str(self):
        return f'${self.balance:,.2f}'


def create_report_emails():
    # TODO: Nicer error handling here
    config = configparser.ConfigParser()
    with open(CONF_DIR / 'config.ini', 'r') as f:
        config.read_file(f)

    try:
        s = lds_session.login()
        report = get_ward_mission_report(s)
        accounts = process_lines(report)
        for account in accounts:
            create_email(config, account)
    except lds_session.AuthError:
        print('Login failed :(')


def get_ward_mission_report(s):
    year = datetime.now().year
    account_id = '14685'  # TODO: How to get internalAccountId?
    url = (
        'https://www.lds.org/finance/income-expenses' 
        f'?fromDate={year}-01-01' 
        f'&toDate={year}-12-31' 
        f'&internalAccountId={account_id}')
    r = s.get(url)
    r.raise_for_status()
    data = r.json()
    for category in data:
        if category['categoryName'] == 'Ward Missionary Fund':
            return category
    raise Exception('Ward Mission Fund not found!')


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


def create_email(config, account):
    to = config['emails'].get(account.name)
    clerk_name = config['emails'].get('clerk_name', 'Ward Clerk')
    summary = account.name + ' ' + account.balance_str
    if to:
        text = EMAIL_BODY.format(summary, clerk_name)
        message = gmail.create_message(
            'me',
            to,
            'Mission account - ' + account.name,
            text,)
        try:
            gmail.create_draft(message)
            print('Email draft created to:', to, summary)
        except Exception as e:
            print('Error creating email draft:', e)
    else:
        print('No email configured for', summary)


if __name__ == '__main__':
    create_report_emails()
