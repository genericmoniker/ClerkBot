import io
from datetime import date
from unittest.mock import Mock

from clerkbot.records import _generate_body

MOVED_IN_DATA = [
    {
        'name': 'Nancy, Charles', 'spokenName': 'Charles Nancy', 'nameOrder': 3,
        'birthDate': '19750322', 'birthDateSort': '19750322', 'gender': 'MALE',
        'genderCode': 1, 'mrn': '0000001234567', 'id': 10000000001,
        'email': 'fatcharlie@gmail.com', 'householdEmail': None,
        'phone': '801-555-1212', 'householdPhone': '801-555-1212',
        'unitNumber': 333333, 'unitName': 'Some Ward',
        'priesthood': 'High Priest', 'priesthoodCode': 6,
        'priesthoodType': 'HIGH_PRIEST', 'age': 43, 'actualAge': 43,
        'actualAgeInMonths': 516, 'genderLabelShort': 'M', 'visible': None,
        'nonMember': False, 'outOfUnitMember': False, 'moveDate': '20180415',
        'hohMrn': '0000001234567', 'addressUnknown': False, 'deceased': False,
        'priorUnit': '222222', 'priorUnitName': 'Some Other Ward',
        'moveDateOrder': 5, 'householdPosition': 'Head of Household',
        'address': '123 Main St, Lehi, Utah 84043',
        'textAddress': '123 Main St, Lehi, Utah 84043',
        'sustainedDate': None, 'formattedMrn': '000-0123-4567',
        'setApart': False
    },
    {
        'name': 'Day, Daisy', 'spokenName': 'Daisy Day',
        'nameOrder': 4, 'birthDate': '19830805', 'birthDateSort': '19830805',
        'gender': 'FEMALE', 'genderCode': 2, 'mrn': '0000012121212',
        'id': 1000000002, 'email': 'officerday@gmail.com',
        'householdEmail': 'officerday@gmail.com', 'phone': '8015552121',
        'householdPhone': '8015552121', 'unitNumber': 333333,
        'unitName': 'Some Ward', 'priesthood': None,
        'priesthoodCode': None, 'priesthoodType': None, 'age': 34,
        'actualAge': 34, 'actualAgeInMonths': 416, 'genderLabelShort': 'F',
        'visible': None, 'nonMember': False, 'outOfUnitMember': False,
        'moveDate': '20180318', 'hohMrn': '0000012121212',
        'addressUnknown': False, 'deceased': False, 'priorUnit': '166901',
        'priorUnitName': 'Some Other Ward', 'moveDateOrder': 0,
        'householdPosition': 'Spouse',
        'address': '321 Main St,<br />Lehi, Utah 84043',
        'textAddress': '321 Main St, Lehi, Utah 84043',
        'sustainedDate': None, 'formattedMrn': '000-1212-1212',
        'setApart': False
    },
]

MOVED_OUT_DATA = [
    {
        'name': 'Nancy, Spider', 'nameOrder': 6, 'birthDate': '19750322',
        'moveDateOrder': 6, 'moveDate': '20180408',
        'priorUnit': 'Some Ward', 'nextUnitName': 'Next Ward',
        'nextUnitNumber': 111111, 'addressUnknown': False, 'deceased': False
    },
    {
        'name': 'Noah, Rose', 'nameOrder': 2, 'birthDate': '19850116',
        'moveDateOrder': 0, 'moveDate': '20180318',
        'priorUnit': 'Some Ward', 'nextUnitName': 'Other Next Ward',
        'nextUnitNumber': 121212, 'addressUnknown': False, 'deceased': False
    },
]


def test_only_includes_changes_since_last_checked():
    s = Mock()
    s.get_members_moved_in.return_value = MOVED_IN_DATA
    s.get_members_moved_out.return_value = MOVED_OUT_DATA
    buffer = io.StringIO()
    last_checked = date(2018, 4, 1)
    _generate_body(s, buffer, last_checked)
    body = buffer.getvalue()
    assert 'Nancy, Charles' in body
    assert 'Day, Daisy' not in body
    assert 'Nancy, Spider' in body
    assert 'Noah, Rose' not in body
