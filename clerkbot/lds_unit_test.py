import json
from pathlib import Path

import pytest

from clerkbot.lds_unit import LDSUnit


@pytest.fixture(name='unit_data')
def unit_data_():
    here = Path(__file__)
    data_file = here.parent / 'test_data' / 'test_unit.json'
    with data_file.open() as f:
        return json.load(f)


def test_get_individual_by_id_head_of_household(unit_data):
    head_of_household_id = 4591147570
    unit = LDSUnit(unit_data)
    individual = unit.get_individual_by_id(head_of_household_id)
    assert individual['fullName'] == 'Francis, Abigail Paul'


def test_get_individual_by_id_spouse(unit_data):
    spouse_id = 8863301856
    unit = LDSUnit(unit_data)
    individual = unit.get_individual_by_id(spouse_id)
    assert individual['fullName'] == 'Burch, Leslie Kimberly'


def test_get_individual_by_id_child(unit_data):
    child_id = 9015469093
    unit = LDSUnit(unit_data)
    individual = unit.get_individual_by_id(child_id)
    assert individual['fullName'] == 'Sharp, Carrie Angela'


def test_get_individuals_by_calling_single(unit_data):
    unit = LDSUnit(unit_data)
    calling = 'Deacons Quorum President'
    individuals = unit.get_individuals_by_calling(calling)
    assert len(individuals) == 1
    assert individuals[0]['fullName'] == 'Myers, Felicia Joseph'


def test_get_individuals_by_calling_multiple(unit_data):
    unit = LDSUnit(unit_data)
    calling = 'Ward Temple and Family History Consultant--Lead'
    individuals = unit.get_individuals_by_calling(calling)
    assert len(individuals) == 2
    assert individuals[0]['fullName'] == 'Perry, Daniel Carol'
    assert individuals[1]['fullName'] == 'Perry, Calvin Daniel'
