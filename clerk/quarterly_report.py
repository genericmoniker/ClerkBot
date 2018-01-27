# -*- coding: utf-8 -*-
"""Script for downloading the "potential" reports for use in compiling the ward
quarterly report. The downloaded PDFs can be sent to the appropriate
organization secretaries so that they can compare their records with the
current headquarters records.

Output is written to '~/Clerk', in a subdirectory named for the quarter.
"""

from datetime import date
import os
from dateutil.relativedelta import relativedelta
import errno

from clerk import lds_session

# If our stake is beta, change 'www' to 'beta':
REPORT_URL = 'https://www.lds.org/mls/mbr/report/'\
             'quarterly-report-details-print'

REPORTS = [
    {
        'line': 14,
        'name': 'Melchizedek Priesthood holders',
    },
    {
        'line': 15,
        'name': 'Prospective elders',
    },
    {
        'line': 16,
        'name': 'Women',
    },
    {
        'line': 17,
        'name': 'Young single adults',
    },
    {
        'line': 18,
        'name': 'Young men',
    },
    {
        'line': 19,
        'name': 'Young women',
    },
    {
        'line': 21,
        'name': 'Children',
    },

    # Not including convert statistics
]


def download_potential_reports(s=None):
    try:
        s = s or lds_session.login()
        year, quarter = last_quarter(date.today())
        report_dir = get_report_dir(year, quarter)
        fetch_reports(s, year, quarter, report_dir)
    except lds_session.AuthError:
        print('Login failed :(')


def last_quarter(today):
    """Get the most recently completed quarter.

    :param today: today's date.
    :return: tuple of year, quarter number
    """
    quarter_date = today - relativedelta(months=1)
    while quarter_date.month % 3 != 0:
        quarter_date = quarter_date - relativedelta(months=1)
    return quarter_date.year, int(quarter_date.month / 3)


def get_report_dir(year, quarter):
    output_dir = os.path.join(os.path.expanduser('~'), 'Clerk')
    path = os.path.join(output_dir, '{}-Q{}'.format(year, quarter))
    print(path)
    try:
        os.makedirs(path)
    except os.error as e:
        if e.errno != errno.EEXIST:
            raise
    return path


def fetch_reports(s, year, quarter, report_dir):
    unit_number = lds_session.get_unit_number(s)
    for report in REPORTS:
        fetch_report(s, unit_number, report, year, quarter, report_dir)


def fetch_report(s, unit_number, report, year, quarter, report_dir):
    name = '{} - {} - Potential.pdf'.format(report['line'], report['name'])
    print(name)
    params = get_report_params(report['line'], unit_number, year, quarter)
    r = s.get(REPORT_URL, params=params, stream=True)
    # print(r.url)
    if r.ok:
        filename = os.path.join(report_dir, name)
        first_chunk = True
        with open(filename, 'wb') as f:
            for chunk in r:
                if first_chunk:
                    if not chunk.startswith(b'%PDF'):
                        print('  ** File isn\'t a PDF! **')
                    first_chunk = False
                f.write(chunk)
    else:
        print(r)


def get_report_params(line, unit_number, year, quarter):
    # The potential reports aren't available until after the quarter ends, so
    # we're asking for the most recently completed quarter.

    # This stuff is subject to change. Try clicking the "Print" button on the
    # report detail page to see what the current parameters should be.
    return {
        'pdf': 'true',
        'lang': 'eng',
        'rowNumber': line,
        'unitNumber': unit_number,
        'showAge': 'false',
        'year': year,
        'quarter': quarter,
        'filter': 'POTENTIAL',
        'sort': 'nameOrder',
    }


if __name__ == '__main__':
    download_potential_reports()
