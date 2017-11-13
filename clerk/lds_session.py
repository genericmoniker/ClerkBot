# -*- coding: utf-8 -*-
import os
import re
from getpass import getpass

import requests


_service_config = None


class AuthError(Exception):
    """Exception raised on auth failure."""
    pass


class UnitError(Exception):
    pass


def service_config():
    """Get the web service configuration.
    :return: deserialized JSON service configuration.
    """
    global _service_config
    if not _service_config:
        r = requests.get('https://tech.lds.org/mobile/ldstools/config.json')
        r.raise_for_status()
        _service_config = r.json()
    return _service_config


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

    # If a beta is in effect, you have to set these cookies to say that you've
    # accepted the terms or you'll get redirected to an acceptance page.
    s.cookies['clerk-resources-beta-eula'] = '4.1'
    s.cookies['clerk-resources-beta-terms'] = 'true'

    url = service_config()['auth-url']
    r = s.post(url, data=data, allow_redirects=False)
    print('Login response: ', r)
    if r.status_code == 200:
        return s
    raise AuthError()


def get_unit_number(s):
    url = service_config()['current-user-unit']
    r = s.get(url)
    r.raise_for_status()
    return r.json()['message']
