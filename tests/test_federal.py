import pytest
from legistream_backend.federal import Stream

def test_federal():
    fed_stream = Stream()
    print('\nHOR stream status: ' + str(fed_stream.lower_is_live))
    print('Senate stream status: ' + str(fed_stream.upper_is_live))
    print('Commitee stream status: ' + str(fed_stream.committee_is_live))
    print(fed_stream.stream_urls)