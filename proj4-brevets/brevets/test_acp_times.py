#nose test

import acp_times
import nose
import logging
import arrow

logging.basicConfig(format='%(levelname)s:%(message)s',level=logging.WARNING)
log = logging.getLogger(__name__)


def test_none():
    DATE = arrow.now()
    assert acp_times.open_time(0,200,DATE.isoformat()) == DATE.shift(hours=+0,minutes=+0).isoformat()
    assert acp_times.close_time(0,200,DATE.isoformat()) == DATE.shift(hours=+1,minutes=+0).isoformat()
def test_case1():
    DATE = arrow.now()
    assert acp_times.open_time(200,200,DATE.isoformat()) == DATE.shift(hours=+5,minutes=+53).isoformat()
    assert acp_times.close_time(200,200,DATE.isoformat()) == DATE.shift(hours=+13,minutes=+30).isoformat()
def test_case2():
    DATE = arrow.now()
    assert acp_times.open_time(550,600,DATE.isoformat()) == DATE.shift(hours=+17,minutes=+8).isoformat()
    assert acp_times.close_time(550,600,DATE.isoformat()) == DATE.shift(hours=+4,minutes=+0).isoformat()
def test_case3():
    DATE = arrow.now()
    assert acp_times.open_time(890,1000,DATE.isoformat()) == DATE.shift(hours=+36,minutes=+40).isoformat()
    assert acp_times.close_time(890,1000,DATE.isoformat()) == DATE.shift(hours=+65,minutes=+23).isoformat()
def test_case4():

    DATE = arrow.now()
    assert acp_times.open_time(890,1000,DATE.isoformat()) == DATE.shift(hours=+36,minutes=+40).isoformat()
    assert acp_times.close_time(890,1000,DATE.isoformat()) == DATE.shift(hours=+65,minutes=+23).isoformat()
