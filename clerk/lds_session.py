import os
from datetime import datetime
from getpass import getpass

import requests


class AuthError(Exception):
    """Exception raised on auth failure."""
    pass


class LDSSession:
    """A session on lds.org.

    See https://github.com/jidn/LDS-org for another programmer's take on this.
    """

    def __init__(self):
        self._s = requests.Session()
        self._service_config = None
        self._unit_number = None
        self.logged_in = False

    @property
    def service_config(self):
        if not self._service_config:
            r = requests.get(
                'https://tech.lds.org/mobile/ldstools/config.json')
            r.raise_for_status()
            self._service_config = r.json()
        return self._service_config

    def login(self):
        """Log in to the lds.org identity server.

        :return: a requests session with cookies set for further operations.

        Reference:
        https://tech.lds.org/wiki/External_Application_Development_with_SSO
        """
        username = os.environ.get('LDS_USERNAME')
        password = os.environ.get('LDS_PASSWORD')
        if username and password:
            print('Using credentials from environment')
        else:
            print('Enter your LDS Account credentials')
            username = input('Username: ')
            password = getpass()
        data = {
            'username': username,
            'password': password,
        }

        # If a beta is in effect, you have to set these cookies to say that
        # you've accepted the terms or you'll get redirected to an acceptance
        # page.
        self._s.cookies['clerk-resources-beta-eula'] = '4.1'
        self._s.cookies['clerk-resources-beta-terms'] = 'true'

        url = self.service_config['auth-url']
        r = self._s.post(url, data=data, allow_redirects=False)
        print('Login response: ', r)
        if r.status_code != 200:
            raise AuthError(r)
        self.logged_in = True

    @property
    def unit_number(self):
        if self._unit_number is None:
            url = self.service_config['current-user-unit']
            r = self._s.get(url)
            r.raise_for_status()
            self._unit_number = r.json()['message']
        return self._unit_number

    def get_unit_data(self, raw=False):
        url_template = self.service_config['unit-members-and-callings-v2']
        url = url_template.replace('%@', self.unit_number)
        r = self._s.get(url)
        r.raise_for_status()
        if raw:
            return r.content
        else:
            return r.json()

    def get_report(self, report, params, stream):
        url = 'https://www.lds.org/mls/mbr/report/' + report
        return self._s.get(url, params=params, stream=stream)

    def get_ward_mission_report(self):
        year = datetime.now().year
        account_id = '14685'  # TODO: How to get internalAccountId?!!
        url = (
            'https://www.lds.org/finance/income-expenses'
            f'?fromDate={year}-01-01'
            f'&toDate={year}-12-31'
            f'&internalAccountId={account_id}')
        r = self._s.get(url)
        r.raise_for_status()
        data = r.json()
        for category in data:
            if category['categoryName'] == 'Ward Missionary Fund':
                return category
        raise Exception('Ward Mission Fund not found!')

    def get_members_moved_in(self):
        """Get a report of members who have moved into the ward.

        """
        # TODO
        # https://beta.lds.org/mls/mbr/services/report/members-moved-in/unit/380695/3?lang=eng
        # 3 means within the past 3 months


class Unit:
    # Dumb brute-force implementations for now...

    def __init__(self, unit_data):
        self.data = unit_data

    def get_org_by_id(self, id_):
        # Organizations are more complicated than this. Need more analysis.
        orgs = self.data['callings']
        for org in orgs:
            if org['typeId'] == id_:
                return org
        return None

    def get_individual_by_id(self, id_):
        directory = self.data['households']
        for household in directory:
            for individual in self._flatten_household(household):
                if individual['individualId'] == id_:
                    return individual
        return None

    @staticmethod
    def _flatten_household(household):
        yield household['headOfHouse']
        if 'spouse' in household:
            yield household['spouse']
        yield from household['children']
