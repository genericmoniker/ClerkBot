import argparse

import sys

from clerkbot import (
    quarterly_report,
    missionary_accounts,
    mailing_labels,
    directory,
    interviews,
    callings,
    records,
)
from clerkbot.lds_session import LDSSession, AuthError


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

    s = LDSSession()
    try:
        s.login()
    except AuthError as e:
        print('Login failed :(', e)
        sys.exit(2)

    if args.c:
        callings.save_callings_snapshot(s)
    if args.d:
        directory.create_directory(s)
    if args.i:
        interviews.create_list_email(s)
    if args.l:
        mailing_labels.create_labels(s)
    if args.ma:
        missionary_accounts.create_report_emails(s)
    if args.qr:
        quarterly_report.download_potential_reports(s)
    if args.r:
        records.create_notification(s)


if __name__ == '__main__':
    main()
