from datetime import date

from clerkbot.quarterly_report import last_quarter


def test_last_quarter_previous_year():
    today = date(2016, 1, 1)
    year, quarter = last_quarter(today)
    assert year == 2015
    assert quarter == 4


def test_last_quarter_current_year():
    today = date(2015, 12, 1)
    year, quarter = last_quarter(today)
    assert year == 2015
    assert quarter == 3


def test_last_quarter_mid_month():
    today = date(2015, 11, 1)
    year, quarter = last_quarter(today)
    assert year == 2015
    assert quarter == 3
