import datetime

import pytest

from extraviadoscli.webscrapers.mor import commons


@pytest.mark.parametrize(
    "datestr,expected",
    [
        ("enero 28, 2018", datetime.date(2018, 1, 28)),
        ("febrero 19, 2018", datetime.date(2018, 2, 19)),
        ("marzo 2, 2018", datetime.date(2018, 3, 2)),
        ("abril 29, 2022", datetime.date(2022, 4, 29)),
        ("mayo 22, 2022", datetime.date(2022, 5, 22)),
        ("junio 13, 2016", datetime.date(2016, 6, 13)),
        ("julio 31, 2016", datetime.date(2016, 7, 31)),
        ("agosto 31, 2016", datetime.date(2016, 8, 31)),
        ("septiembre 27, 2016", datetime.date(2016, 9, 27)),
        ("octubre 28, 2021", datetime.date(2021, 10, 28)),
        ("noviembre 1, 2016", datetime.date(2016, 11, 1)),
        ("diciembre 15, 2016", datetime.date(2016, 12, 15)),
    ],
)
def test_parsedate(datestr, expected):
    result = commons.parse_date(datestr)
    assert result == expected
