# -*- coding: utf-8 -*-

from getpass import getpass
from datetime import date
import os
from dateutil.relativedelta import relativedelta
import errno
import requests
import time

from clerk import lds_session

REPORT_URL = 'https://beta.lds.org/mls/mbr/report/quarterly-report/details/'
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


def download_potential_reports():
    try:
        s = lds_session.login()
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
    for report in REPORTS:
        fetch_report(s, report, year, quarter, report_dir)


def fetch_report(s, report, year, quarter, report_dir):
    name = '{} - {} - Potential.pdf'.format(report['line'], report['name'])
    print(name)
    url = REPORT_URL + str(report['line'])
    params = get_report_params(year, quarter)
    r = s.get(url, params=params, stream=True)
    if r.ok:
        filename = os.path.join(report_dir, name)
        with open(filename, 'wb') as f:
            for chunk in r:
                f.write(chunk)
    else:
        print(r.text)


def get_report_params(year, quarter):
    # The potential reports aren't available until after the quarter ends, so
    # we're asking for the most recently completed quarter.
    return {
        'lang': 'eng',
        'pdf': 'true',
        'sort': 'name',
        'sortDir': '0',
        'showAge': 'false',
        'filter': 'POTENTIAL',
        'date': time.time(),
        'year': year,
        'quarter': quarter,
    }
