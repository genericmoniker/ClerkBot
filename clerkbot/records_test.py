import io
from datetime import date
from unittest.mock import Mock

from clerkbot.records import _generate_body, _get_members_moved

MOVED_IN_DATA = [
    {
        'name': 'Nancy, Charles',
        'spokenName': 'Charles Nancy',
        'nameOrder': 3,
        'birthDate': '19750322',
        'birthDateSort': '19750322',
        'gender': 'MALE',
        'genderCode': 1,
        'mrn': '0000001234567',
        'id': 10000000001,
        'email': 'fatcharlie@gmail.com',
        'householdEmail': None,
        'phone': '801-555-1212',
        'householdPhone': '801-555-1212',
        'unitNumber': 333333,
        'unitName': 'Some Ward',
        'priesthood': 'High Priest',
        'priesthoodCode': 6,
        'priesthoodType': 'HIGH_PRIEST',
        'age': 43,
        'actualAge': 43,
        'actualAgeInMonths': 516,
        'genderLabelShort': 'M',
        'visible': None,
        'nonMember': False,
        'outOfUnitMember': False,
        'moveDate': '20180415',
        'hohMrn': '0000001234567',
        'addressUnknown': False,
        'deceased': False,
        'priorUnit': '222222',
        'priorUnitName': 'Some Other Ward',
        'moveDateOrder': 5,
        'householdPosition': 'Head of Household',
        'address': '123 Main St, Lehi, Utah 84043',
        'textAddress': '123 Main St, Lehi, Utah 84043',
        'sustainedDate': None,
        'formattedMrn': '000-0123-4567',
        'setApart': False,
    },
    {
        'name': 'Day, Daisy',
        'spokenName': 'Daisy Day',
        'nameOrder': 4,
        'birthDate': '19830805',
        'birthDateSort': '19830805',
        'gender': 'FEMALE',
        'genderCode': 2,
        'mrn': '0000012121212',
        'id': 1000000002,
        'email': 'officerday@gmail.com',
        'householdEmail': 'officerday@gmail.com',
        'phone': '8015552121',
        'householdPhone': '8015552121',
        'unitNumber': 333333,
        'unitName': 'Some Ward',
        'priesthood': None,
        'priesthoodCode': None,
        'priesthoodType': None,
        'age': 34,
        'actualAge': 34,
        'actualAgeInMonths': 416,
        'genderLabelShort': 'F',
        'visible': None,
        'nonMember': False,
        'outOfUnitMember': False,
        'moveDate': '20180318',
        'hohMrn': '0000012121212',
        'addressUnknown': False,
        'deceased': False,
        'priorUnit': '166901',
        'priorUnitName': 'Some Other Ward',
        'moveDateOrder': 0,
        'householdPosition': 'Spouse',
        'address': '321 Main St,<br />Lehi, Utah 84043',
        'textAddress': '321 Main St, Lehi, Utah 84043',
        'sustainedDate': None,
        'formattedMrn': '000-1212-1212',
        'setApart': False,
    },
]

MOVED_OUT_DATA = [
    {
        'name': 'Nancy, Spider',
        'nameOrder': 6,
        'birthDate': '19750322',
        'moveDateOrder': 6,
        'moveDate': '20180408',
        'priorUnit': 'Some Ward',
        'nextUnitName': 'Next Ward',
        'nextUnitNumber': 111111,
        'addressUnknown': False,
        'deceased': False,
    },
    {
        'name': 'Noah, Rose',
        'nameOrder': 2,
        'birthDate': '19850116',
        'moveDateOrder': 0,
        'moveDate': '20180318',
        'priorUnit': 'Some Ward',
        'nextUnitName': 'Other Next Ward',
        'nextUnitNumber': 121212,
        'addressUnknown': False,
        'deceased': False,
    },
]


def _setup(moved_in, moved_out):
    s = Mock()
    s.get_members_moved_in.return_value = moved_in
    s.get_members_moved_out.return_value = moved_out
    return s, io.StringIO()


def test_members_moved():
    members = [
        {'name': 'Third', 'moveDate': '20190503'},
        {'name': 'Fourth', 'moveDate': '20190504'},
        {'name': 'Fifth', 'moveDate': '20190505'},
        {'name': 'Sixth', 'moveDate': '20190506'},
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
    s, buffer = _setup(MOVED_IN_DATA, MOVED_OUT_DATA)
    last_checked = date(2018, 4, 1)
    until = date(2018, 4, 16)
    _generate_body(s, buffer, last_checked, until)
    body = buffer.getvalue()
    assert 'Day, Daisy' not in body  # moveDate: 20180318
    assert 'Noah, Rose' not in body  # moveDate: 20180318
    assert 'Nancy, Spider' in body   # moveDate: 20180408
    assert 'Nancy, Charles' in body  # moveDate: 20180415


def test_limited_by_until_param():
    s, buffer = _setup([], MOVED_OUT_DATA)
    last_checked = date(2018, 3, 17)
    until = date(2018, 4, 8)
    _generate_body(s, buffer, last_checked, until)
    body = buffer.getvalue()
    assert 'Noah, Rose' in body
    assert 'Nancy, Spider' not in body


def test_daily_run_catches_moved_records():
    moved_out_data = [
        {
            'name': 'Move Feb 21',
            'nameOrder': 6,
            'birthDate': '19800101',
            'moveDateOrder': 6,
            'moveDate': '20190221',
            'priorUnit': 'Some Ward',
            'nextUnitName': 'Next Ward',
            'nextUnitNumber': 111111,
            'addressUnknown': False,
            'deceased': False,
        },
        {
            'name': 'Move Feb 22',
            'nameOrder': 6,
            'birthDate': '19800101',
            'moveDateOrder': 6,
            'moveDate': '20190222',
            'priorUnit': 'Some Ward',
            'nextUnitName': 'Next Ward',
            'nextUnitNumber': 111111,
            'addressUnknown': False,
            'deceased': False,
        },
        {
            'name': 'Move Feb 23',
            'nameOrder': 6,
            'birthDate': '19800101',
            'moveDateOrder': 6,
            'moveDate': '20190223',
            'priorUnit': 'Some Ward',
            'nextUnitName': 'Next Ward',
            'nextUnitNumber': 111111,
            'addressUnknown': False,
            'deceased': False,
        },
    ]
    s, buffer = _setup([], moved_out_data)
    last_checked = date(2019, 2, 22)
    today = date(2019, 2, 23)
    _generate_body(s, buffer, last_checked, today)
    body = buffer.getvalue()
    assert 'Move Feb 21' not in body
    assert 'Move Feb 22' in body
    assert 'Move Feb 23' not in body


def test_prior_unit_unknown_is_formatted_appropriately():
    moved_in_data = MOVED_IN_DATA.copy()
    moved_in_data[0]['priorUnit'] = None
    moved_in_data[0]['priorUnitName'] = None
    s, buffer = _setup(moved_in_data, [])
    last_checked = date(2018, 2, 21)
    until = date(2018, 4, 30)
    _generate_body(s, buffer, last_checked, until)
    body = buffer.getvalue()
    assert 'None' not in body
    assert 'unknown unit' in body
