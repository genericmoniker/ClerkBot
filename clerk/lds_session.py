# -*- coding: utf-8 -*-
import os
from getpass import getpass

import requests

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
    r = s.post(LOGIN_URL, data=data, allow_redirects=False)
    if r.ok:
        return s
    raise AuthError()
