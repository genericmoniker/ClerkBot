import io
from contextlib import contextmanager


def create_report(s):
    buffer = io.StringIO()
    _generate_body(s, buffer)
    body = buffer.getvalue()
    buffer.close()
    print(body)


def _generate_body(s, buffer):
    moved_in = s.get_members_moved_in()
    if moved_in:
        print('These records have been moved into the ward:', file=buffer)
        for mi in moved_in:
            print(
                '-', mi['name'],
                'from the', mi['priorUnitName'],
                file=buffer
            )
        print()
    moved_out = s.get_members_moved_out()
    if moved_out:
        print('These records have been moved out of the ward:', file=buffer)
        for mo in moved_out:
            print(
                '-', mo['name'],
                'to the', mo['nextUnitName'],
                file=buffer
            )


@contextmanager
def last_checked():
    pass
