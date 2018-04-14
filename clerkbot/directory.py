"""Handle the basic formatting for a concise printed member directory."""
from clerkbot import lds_session
from clerkbot.lds_session import Unit
from clerkbot.paths import OUTPUT_DIR


def begin_rtf(rtf_file):
    rtf_file.write(r'{\rtf1\ansi\deff0')


def write_households(rtf_file, directory):
    for record in directory:
        write_people_line(rtf_file, record)


def write_people_line(rtf_file, record):
    phone = record.get('phone', '')
    names = record['coupleName']
    parts = names.split(',')
    rtf_file.write(r'\b {}\b0,{} \tab {}\line'.format(
        parts[0], parts[1], phone)
    )
    rtf_file.write('\r\n')


def write_leadership(rtf_file, unit):
    org_ids = [
        1179,  # bishopric
    ]
    for org_id in org_ids:
        org = unit.get_org_by_id(org_id)
        for calling in org['children']:
            pass


def end_rtf(rtf_file):
    rtf_file.write('}')


def create_directory(s):
    assert s.logged_in, 'Expected logged in session.'
    data = s.get_unit_data()
    unit = Unit(data)

    file = OUTPUT_DIR / 'directory.rtf'
    with file.open('w') as f:
        begin_rtf(f)
        write_households(f, unit.data['households'])
        # TODO
        # write_leadership(f, unit)
        end_rtf(f)

    print('Directory written to', file)
