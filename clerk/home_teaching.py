# -*- coding: utf-8 -*-
"""Script for downloading home teaching reports.
"""

import errno
import os

from clerk import lds_session

OUTPUT_DIR = os.path.join(os.path.expanduser('~'), 'Clerk')
HT_URL = (
    'https://beta.lds.org/htvt/services/v1/{{}}/print?auxiliaryId={}&'
    'reportType=OVERVIEW&printPercent=true&overviewCategories='
    'STATS_BY_MONTH%2CNOT_VISITED%2CPOTENTIAL_HOUSEHOLDS_UNASSIGNED%2C'
    'POTENTIAL_TEACHERS_UNASSIGNED&lang=eng'
)
DEACONS_URL = (
    'https://beta.lds.org/mls/mbr/orgs/534259/print?unitNumber={}&'
    'lang=eng&pdf=true'
)

REPORTS = [
    {
        'name': 'High Priests Home Teaching',
        'url': HT_URL.format(534256)
    },
    {
        'name': 'Elders Home Teaching',
        'url': HT_URL.format(534257)
    },
    {
        'name': 'Deacons Quorum Members',
        'url': DEACONS_URL,
        'form_data': dict(
            unitNumber=None,
            subOrgId=534259,
            vacant='',
            filled='',
            notSetApart='',
            custom='',
            hidden='',
            yearsInCalling=0,
            parentSubOrgIdsFilter='534274,4328260',
            expandedResponsibilities='',
            groupByOrg=True,
            membersShowGender=False,
            membersShowAge=True,
            membersShowPhone=True,
            membersShowEmail=True,
            membersShowAddress=False,
            membersShowCurrentUnit=False,
            membersMinAge='',
            membersMaxAge='',
            includeMembers=True,
            includeCallings=False,
            includeHtvt=False,
            filterPositionTypes='',
            selectedMemberIndividualIds='',
            membersSort='birthdate',
            membersSortDir=0,
            membersFilterPriesthood='',
            callingsSort='sequence',
            callingsSortDir=0)
    },
]


def download_reports():
    try:
        s = lds_session.login()
        report_dir = get_report_dir()
        fetch_reports(s, report_dir)
    except lds_session.AuthError:
        print('Login failed :(')
    except UnitError as e:
        print('Error finding unit number: ' + str(e))


def get_report_dir():
    output_dir = os.path.join(os.path.expanduser('~'), 'Clerk')
    path = os.path.join(output_dir, 'Home Teaching')
    print('Output path: ', path)
    try:
        os.makedirs(path)
    except os.error as e:
        if e.errno != errno.EEXIST:
            raise
    return path


def fetch_reports(s, report_dir):
    unit_number = lds_session.get_unit_number(s)
    for report in REPORTS:
        fetch_report(s, unit_number, report, report_dir)


def fetch_report(s, unit_number, report, report_dir):
    name = '{}.pdf'.format(report['name'])
    print(name)
    url = report['url'].format(unit_number)
    try:
        data = report['form_data']
        data['unitNumber'] = unit_number
        r = s.post(url, data=data, stream=True)
    except KeyError:
        r = s.get(url, stream=True)
    if r.ok:
        filename = os.path.join(report_dir, name)
        with open(filename, 'wb') as f:
            for chunk in r:
                f.write(chunk)
    else:
        print(r.text)


if __name__ == '__main__':
    download_reports()
