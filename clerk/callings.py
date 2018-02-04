import datetime

from clerk import lds_session
from clerk.paths import OUTPUT_DIR


def save_callings_snapshot(s=None):
    try:
        s = s or lds_session.login()
        unit = lds_session.get_unit_number(s)
        callings = lds_session.get_unit_data(s, unit, raw=True)
        now = datetime.datetime.now().replace(microsecond=0)
        now_format = now.isoformat().replace(':', '')
        out_dir = OUTPUT_DIR / 'callings'
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / (now_format + '.json')
        out_file.write_bytes(callings)
        print('Callings written to', out_file)
    except lds_session.AuthError:
        print('Login failed :(')


if __name__ == '__main__':
    save_callings_snapshot()
