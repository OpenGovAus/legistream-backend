import pytest
from legistream_backend.nt import Stream

nt_stream = Stream()

def test_nt():
    print('\nNT Lower House stream status: ' + str(nt_stream.lower_is_live))
    print('NT Lower stream URL: ' + nt_stream.lower_stream_url)
    print(nt_stream.stream_urls)