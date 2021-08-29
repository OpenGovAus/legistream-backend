import pytest


from datetime import datetime
from typing import Dict, List


from legistream_backend.util import url_re
from legistream_backend.site.tas import SittingCalendar


def test_cal():
    calendar = SittingCalendar('https://www.parliament.tas.gov.au/')
    print(calendar)
    print(repr(calendar))
    assert isinstance(calendar.sitting_days, List)
    assert isinstance(calendar.all_days, Dict)

    for day in calendar.all_days.keys():
        assert isinstance(day, int)
        assert datetime.fromtimestamp(day)
        this_day = calendar.all_days[day]
        assert isinstance(this_day, Dict)
        for house in this_day.keys():
            assert house in ['lower', 'upper']
            assert isinstance(this_day[house], bool)

    for sitting_day in calendar.sitting_days:
        assert isinstance(sitting_day, int)
        assert datetime.fromtimestamp(sitting_day)
