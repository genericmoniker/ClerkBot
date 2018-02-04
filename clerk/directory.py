"""Handle the basic formatting for a concise printed member directory."""
from clerk import lds_session
from clerk.paths import OUTPUT_DIR


def begin_rtf(rtf_file):
    rtf_file.write(r'{\rtf1\ansi\deff0')


def write_people_line(rtf_file, record):
    phone = record.get('phone', '')
    names = record['coupleName']
    parts = names.split(',')
    rtf_file.write(r'\b {}\b0,{} \tab {}\line'.format(
        parts[0], parts[1], phone)
    )
    rtf_file.write('\r\n')


def end_rtf(rtf_file):
    rtf_file.write('}')


def create_directory(s=None):
    s = s or lds_session.login()
    unit = lds_session.get_unit_number(s)
    directory = lds_session.get_unit_data(s, unit)['households']

    file = OUTPUT_DIR / 'directory.rtf'
    with file.open('w') as f:
        begin_rtf(f)

        for record in directory:
            write_people_line(f, record)

        end_rtf(f)

    print('Directory written to', file)


if __name__ == '__main__':
    create_directory()
