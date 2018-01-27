import argparse

import sys

from clerk import home_teaching, quarterly_report, missionary_accounts, \
    mailing_labels, directory, lds_session


def main():
    parser = argparse.ArgumentParser(description='Clerk Tools')
    parser.add_argument('-d, --directory',
                        dest='d',
                        help='Generate concise directory of households',
                        action='store_true')
    parser.add_argument('-l, --labels',
                        dest='l',
                        help='Generate mailing labels to households',
                        action='store_true')
    parser.add_argument('-m, --missionary-accounts',
                        dest='ma',
                        help='Send missionary account balance emails',
                        action='store_true')
    parser.add_argument('-t, --home-teaching',
                        dest='ht',
                        help='Download home teaching reports',
                        action='store_true')
    parser.add_argument('-q, --quarterly-report',
                        dest='qr',
                        help='Download the quarterly potential reports',
                        action='store_true')

    # Help if no args were passed.
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    try:
        s = lds_session.login()
    except lds_session.AuthError:
        print('Login failed :(')
        sys.exit(2)

    if args.d:
        directory.create_directory(s)
    if args.l:
        mailing_labels.create_labels(s)
    if args.ma:
        missionary_accounts.create_report_emails(s)
    if args.ht:
        home_teaching.download_reports(s)
    if args.qr:
        quarterly_report.download_potential_reports(s)


if __name__ == '__main__':
    main()
