import datetime

from clerkbot.paths import OUTPUT_DIR


def save_callings_snapshot(s):
    assert s.logged_in, 'Expected logged in session.'
    callings = s.get_unit_data(raw=True)
    now = datetime.datetime.now().replace(microsecond=0)
    now_format = now.isoformat().replace(':', '')
    out_dir = OUTPUT_DIR / 'callings'
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / (now_format + '.json')
    out_file.write_bytes(callings)
    print('Callings written to', out_file)
