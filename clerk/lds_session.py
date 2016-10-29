# -*- coding: utf-8 -*-
import os
import re
from getpass import getpass

import requests

from clerk.home_teaching import UnitError

LOGIN_URL = 'https://signin.lds.org/login.html'


class AuthError(Exception):
    """Exception raised on auth failure."""
    pass


def login():
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
    s = requests.Session()

    # If a beta is in effect, you have to set this cookie to say that you've
    # accepted the terms or you'll get redirected to an acceptance page.
    s.cookies['clerk-resources-beta-terms'] = 'true'

    r = s.post(LOGIN_URL, data=data, allow_redirects=False)
    print('Login response: ', r)
    if r.status_code == 200:
        return s
    raise AuthError()


def get_unit_number(s):
    # Scrape the unit number from the main page.
    r = s.get('https://www.lds.org/mls/mbr/?lang=eng')
    if not r.ok:
        raise UnitError(r.reason)
    try:
        return re.search(r"unitNumber\":(\d+)", r.text).group(1)
    except (IndexError, AttributeError):
        raise UnitError('Unit number not found')
