import pytest
from legistream_backend.act_stream import Stream

def test_act():
    stream_data = Stream()
    print('\n' + stream_data.lower_stream_url)
    print('Is the ACT LA live? ' + str(stream_data.is_live))