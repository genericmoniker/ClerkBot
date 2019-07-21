import io
from datetime import date
from unittest.mock import Mock

from clerkbot.records import _generate_body, _get_members_moved

MOVED_IN_DATA = [
    {
        'address': '123 Main St<br />Lehi, Utah 84043',
        'addressUnknown': False,
        'age': 44,
        'birthdate': '14 Jul 1975',
        'birthdateCalc': '1975-07-14',
        'gender': 'M',
        'genderLabelShort': 'M',
        'householdPosition': 'Head of Household',
        'householdPositionEnum': 'HEAD',
        'householdUuid': 'aaaaaaaa-eeee-4444-9999-aaaaaaaaaaaa',
        'id': 10000000001,
        'locale': 'en',
        'moveDate': '15 Apr 2018',
        'moveDateCalc': '2018-04-15',
        'moveDateOrder': 27,
        'name': 'Nancy, Charles',
        'nameOrder': 5,
        'phone': '801-555-1212 his',
        'priesthood': None,
        'priorUnitName': 'Some Other Unit',
        'priorUnitNumber': '444444',
        'textAddress': '123 Main St, Lehi, Utah 84043',
        'unitName': 'Some Ward',
    },
    {
        'address': '123 Main St<br />Lehi, Utah 84043',
        'addressUnknown': False,
        'age': 43,
        'birthdate': '23 Aug 1975',
        'birthdateCalc': '1975-08-23',
        'gender': 'F',
        'genderLabelShort': 'F',
        'householdPosition': 'Spouse',
        'householdPositionEnum': 'SPOUSE',
        'householdUuid': 'aaaaaaaa-eeee-4444-9999-aaaaaaaaaaaa',
        'id': 10000000002,
        'locale': 'en',
        'moveDate': '03 Mar 2018',
        'moveDateCalc': '2018-03-18',
        'moveDateOrder': 22,
        'name': 'Day, Daisy',
        'nameOrder': 2,
        'phone': '801-555-1213 home',
        'priesthood': None,
        'priorUnitName': 'Some Other Ward',
        'priorUnitNumber': '444444',
        'textAddress': '123 Main St, Lehi, Utah 84043',
        'unitName': 'Some Ward',
    },
]

MOVED_OUT_DATA = [
    {
        'addressUnknown': False,
        'birthDate': '1990-05-16',
        'birthDateDisplay': '16 May 1990',
        'deceased': False,
        'moveDate': '2018-04-08',
        'moveDateDisplay': '08 Apr 2018',
        'moveDateOrder': 0,
        'name': 'Nancy, Spider',
        'nameOrder': 2,
        'nextUnitName': 'Next Ward',
        'nextUnitNumber': 2000000,
        'priorUnit': 'Some Ward',
    },
    {
        'addressUnknown': False,
        'birthDate': '1996-05-16',
        'birthDateDisplay': '16 May 1996',
        'deceased': False,
        'moveDate': '2018-03-18',
        'moveDateDisplay': '18 Mar 2018',
        'moveDateOrder': 0,
        'name': 'Noah, Rose',
        'nameOrder': 2,
        'nextUnitName': 'Other Next Ward',
        'nextUnitNumber': 3000000,
        'priorUnit': 'Some Ward',
    },
]


def _setup(moved_in, moved_out):
    lcr = Mock()
    lcr.members_moved_in.return_value = moved_in
    lcr.members_moved_out.return_value = moved_out
    return lcr, io.StringIO()


def test_members_moved():
    members = [
        {'name': 'Third', 'moveDate': '2019-05-03'},
        {'name': 'Fourth', 'moveDate': '2019-05-04'},
        {'name': 'Fifth', 'moveDate': '2019-05-05'},
        {'name': 'Sixth', 'moveDate': '2019-05-06'},
    ]

    since = date(2019, 5, 3)
    until = date(2019, 5, 7)
    moved = str(_get_members_moved(members, since, until))
    assert 'Third' in moved
    assert 'Fourth' in moved
    assert 'Fifth' in moved
    assert 'Sixth' in moved

    since = date(2019, 5, 4)
    until = date(2019, 5, 5)
    moved = str(_get_members_moved(members, since, until))
    assert 'Third' not in moved
    assert 'Fourth' in moved
    assert 'Fifth' not in moved
    assert 'Sixth' not in moved


def test_only_includes_changes_since_last_checked():
    lcr, buffer = _setup(MOVED_IN_DATA, MOVED_OUT_DATA)
    last_checked = date(2018, 4, 1)
    until = date(2018, 4, 16)
    _generate_body(lcr, buffer, last_checked, until)
    body = buffer.getvalue()
    assert 'Day, Daisy' not in body  # moveDate: 20180318
    assert 'Noah, Rose' not in body  # moveDate: 20180318
    assert 'Nancy, Spider' in body  # moveDate: 20180408
    assert 'Nancy, Charles' in body  # moveDate: 20180415


def test_limited_by_until_param():
    lcr, buffer = _setup([], MOVED_OUT_DATA)
    last_checked = date(2018, 3, 17)
    until = date(2018, 4, 8)
    _generate_body(lcr, buffer, last_checked, until)
    body = buffer.getvalue()
    assert 'Noah, Rose' in body
    assert 'Nancy, Spider' not in body


def test_daily_run_catches_moved_records():
    moved_out_data = [
        {
            'name': 'Move Feb 21',
            'nameOrder': 6,
            'birthDate': '1980-01-01',
            'moveDateOrder': 6,
            'moveDate': '2019-02-21',
            'priorUnit': 'Some Ward',
            'nextUnitName': 'Next Ward',
            'nextUnitNumber': 111111,
            'addressUnknown': False,
            'deceased': False,
        },
        {
            'name': 'Move Feb 22',
            'nameOrder': 6,
            'birthDate': '1980-01-01',
            'moveDateOrder': 6,
            'moveDate': '2019-02-22',
            'priorUnit': 'Some Ward',
            'nextUnitName': 'Next Ward',
            'nextUnitNumber': 111111,
            'addressUnknown': False,
            'deceased': False,
        },
        {
            'name': 'Move Feb 23',
            'nameOrder': 6,
            'birthDate': '1980-01-01',
            'moveDateOrder': 6,
            'moveDate': '2019-02-23',
            'priorUnit': 'Some Ward',
            'nextUnitName': 'Next Ward',
            'nextUnitNumber': 111111,
            'addressUnknown': False,
            'deceased': False,
        },
    ]
    lcr, buffer = _setup([], moved_out_data)
    last_checked = date(2019, 2, 22)
    today = date(2019, 2, 23)
    _generate_body(lcr, buffer, last_checked, today)
    body = buffer.getvalue()
    assert 'Move Feb 21' not in body
    assert 'Move Feb 22' in body
    assert 'Move Feb 23' not in body


def test_prior_unit_unknown_is_formatted_appropriately():
    moved_in_data = MOVED_IN_DATA.copy()
    moved_in_data[0]['priorUnit'] = None
    moved_in_data[0]['priorUnitName'] = None
    lcr, buffer = _setup(moved_in_data, [])
    last_checked = date(2018, 2, 21)
    until = date(2018, 4, 30)
    _generate_body(lcr, buffer, last_checked, until)
    body = buffer.getvalue()
    assert 'None' not in body
    assert 'unknown unit' in body


def test_next_unit_unknown_is_formatted_appropriately():
    moved_out_data = MOVED_OUT_DATA.copy()
    moved_out_data[0]['nextUnitNumber'] = None
    moved_out_data[0]['nextUnitName'] = None
    moved_out_data[0]['addressUnknown'] = True
    lcr, buffer = _setup([], moved_out_data)
    last_checked = date(2018, 2, 21)
    until = date(2018, 4, 30)
    _generate_body(lcr, buffer, last_checked, until)
    body = buffer.getvalue()
    assert 'None' not in body
    assert 'unknown unit' in body
