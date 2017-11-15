import argparse

from clerk import home_teaching, quarterly_report, missionary_accounts


def main():
    parser = argparse.ArgumentParser(description='Clerk Tools')
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
    args = parser.parse_args()
    if args.ma:
        missionary_accounts.create_report_emails()
    if args.ht:
        home_teaching.download_reports()
    if args.qr:
        quarterly_report.download_potential_reports()


if __name__ == '__main__':
    main()
