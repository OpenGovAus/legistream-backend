import pytest
from legistream_backend.wa import Stream

wa_stream = Stream()

def test_wa():
    print('\nWA Lower stream status: ' + str(wa_stream.lower_is_live))
    print('WA Upper stream status: ' + str(wa_stream.upper_is_live))
    print(str(wa_stream.stream_urls))