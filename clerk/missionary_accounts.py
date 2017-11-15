"""Create email reports of missionary balances.

"""
import configparser
from datetime import datetime

from clerk import lds_session, gmail
from clerk.paths import CONF_DIR


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
    summary = account.name + ' ' + account.balance_str
    if to:
        text = summary  # TODO: Real email message
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
