import pytest
from legistream_backend.nsw import Stream

nsw_stream = Stream()

def test_nsw_stream_status():
    print('\nNSW Lower House stream status: ' + str(nsw_stream.lower_is_live))
    print('NSW Upper House stream status: ' + str(nsw_stream.upper_is_live))
    print('NSW Committee stream status: ' + str(nsw_stream.committee_is_live))
    print('NSW Jubilee Room stream status: ' + str(nsw_stream.jubilee_is_live))

def test_nsw_stream_urls():
    print('\nJubilee: ' + nsw_stream.jubilee_stream_url)
    print('Committee: ' + nsw_stream.committe_stream_url)
    print('LA: ' + nsw_stream.lower_stream_url)
    print('LC: ' + nsw_stream.upper_stream_url)
    print(nsw_stream.stream_urls)