import argparse
import os
import sys

from getpass import getpass

from clerkbot import (
    quarterly_report,
    missionary_accounts,
    mailing_labels,
    directory,
    interviews,
    callings,
    records,
)
from clerkbot.lcr_plus import API
from lcr import InvalidCredentialsError


def main():
    parser = argparse.ArgumentParser(description='ClerkBot')
    parser.add_argument(
        '-c, --callings',
        dest='c',
        help='Save a snapshot of current callings',
        action='store_true',
    )
    parser.add_argument(
        '-d, --directory',
        dest='d',
        help='Generate concise directory of households',
        action='store_true',
    )
    parser.add_argument(
        '-i, --interviews',
        dest='i',
        help='Send the action',
        action='store_true',
    )
    parser.add_argument(
        '-l, --labels',
        dest='l',
        help='Generate mailing labels to households',
        action='store_true',
    )
    parser.add_argument(
        '-m, --missionary-accounts',
        dest='ma',
        help='Send missionary account balance emails',
        action='store_true',
    )
    parser.add_argument(
        '-q, --quarterly-report',
        dest='qr',
        help='Download the quarterly potential reports',
        action='store_true',
    )
    parser.add_argument(
        '-r, --records',
        dest='r',
        help='Email a report of records moved in or out',
        action='store_true',
    )

    # Help if no args were passed.
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    username, password, unit_number = get_credentials()
    try:
        lcr = API(username, password, unit_number, beta=True)
    except InvalidCredentialsError as e:
        print('Login failed :(', e)
        sys.exit(2)

    # Disabled for now...
    # if args.c:
    #     callings.save_callings_snapshot(s)
    # if args.d:
    #     directory.create_directory(s)
    # if args.i:
    #     interviews.create_list_email(s)
    # if args.l:
    #     mailing_labels.create_labels(s)
    if args.ma:
        missionary_accounts.create_report_emails(lcr)
    if args.qr:
        quarterly_report.download_potential_reports(lcr)
    if args.r:
        records.create_notification(lcr)


def get_credentials():
    username = os.environ.get('LDS_USERNAME')
    password = os.environ.get('LDS_PASSWORD')
    unit_number = os.environ.get('LDS_UNIT_NUMBER')
    if username and password:
        print('Using credentials from environment')
    else:
        print('Enter your LDS Account credentials')
        username = input('Username: ')
        password = getpass()
        unit_number = input('Unit number: ')
    return username, password, unit_number


if __name__ == '__main__':
    main()
