import pytest
from legistream_backend.sa import Stream

sa_stream = Stream()

def test_sa():
    print('\nSA Lower House stream status: ' + str(sa_stream.lower_is_live))
    print('SA Upper House stream status: ' + str(sa_stream.upper_is_live))
    print('SA Lower stream URL: ' + sa_stream.lower_stream_url)
    print('SA Upper stream URL: ' + sa_stream.upper_stream_url)
    print(sa_stream.stream_urls)