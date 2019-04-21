"""
Stand-alone script to scrub ("anonymize") unit data.

Note that the scrubbed data isn't necessarily consistent:
- A person may end up with names that are not gender consistent.
- Parts of addresses are not geographically consistent.

Run without arguments to see usage.
"""
import json
import random
import sys

from faker import Faker
from faker.providers.address import Provider as BaseProvider


class Provider(BaseProvider):
    """Provider for fake values."""

    def individual_id(self):
        return self.random_int(max=10 ** 10)

    def member_id(self):
        return self.numerify(text='###-####-####')

    def latitude(self):
        return random.uniform(-90, 90)

    def longitude(self):
        return random.uniform(-180, 180)


fake = Faker()
fake.add_provider(Provider)


def main():
    try:
        in_file = sys.argv[1]
        out_file = sys.argv[2]
    except IndexError:
        print_usage()
        exit(1)
    else:
        scrub(in_file, out_file)


def print_usage():
    print('Usage:')
    print('scrub <input JSON file> <output JSON file>')
    print()


def scrub(in_file, out_file):
    with open(in_file) as f:
        data = json.load(f)
    scrub_unit(data)
    ids = scrub_households(data)
    scrub_callings(data, ids)

    with open(out_file, 'w') as f:
        json.dump(data, f, indent=2)


def scrub_unit(data):
    data['unitNo'] = 12345
    data['orgName'] = 'Test Unit'


def scrub_households(data):
    ids = dict()
    households = data['households']
    for household in households:
        last = fake.last_name()
        household['householdName'] = last
        household['headOfHouseIndividualId'] = ids.setdefault(
            household['headOfHouseIndividualId'], fake.individual_id()
        )
        scrub_address(household)
        first = scrub_person(household['headOfHouse'], last, ids)
        if 'spouse' in household:
            spouse_name = scrub_person(household['spouse'], last, ids)
            household['coupleName'] = f'{last}, {first} & {spouse_name}'
        else:
            household['coupleName'] = f'{last}, {first}'
        if 'children' in household:
            for child in household['children']:
                scrub_person(child, last, ids)
    return ids


def scrub_address(household):
    zipcode = fake.zipcode_plus4()
    household['desc1'] = fake.street_address()
    if 'desc2' in household:
        household['desc2'] = fake.secondary_address()
    household['desc3'] = f'{fake.city()}, {fake.state_abbr()} {zipcode}'
    household['state'] = fake.state()
    household['postalCode'] = zipcode
    household['latitude'] = fake.latitude()
    household['longitude'] = fake.longitude()


def scrub_person(person, last, ids):
    last = last or fake.last_name()
    first = fake.first_name()
    middle = fake.first_name()
    person['fullName'] = f'{last}, {first} {middle}'
    person['preferredName'] = f'{last}, {first}'
    person['memberId'] = fake.member_id()
    person['individualId'] = ids.setdefault(
        person['individualId'], fake.individual_id()
    )
    person['surname'] = last
    person['givenName'] = f'{first} {middle}'
    person['phone'] = fake.phone_number()
    person['email'] = fake.email()
    return first


def scrub_callings(data, ids):
    for org in data['callings']:
        scrub_org(org, ids)


def scrub_org(org, ids):
    for key in org.keys():
        if key == 'children':
            for org in org['children']:
                scrub_org(org, ids)
        elif key == 'assignmentsInGroup':
            assignments = org['assignmentsInGroup']
            for assignment in assignments:
                try:
                    mapped_id = ids[assignment['individualId']]
                    assignment['individualId'] = mapped_id
                except KeyError:
                    pass


if __name__ == '__main__':
    main()
