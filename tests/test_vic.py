from legistream_backend.vic import Stream
import pytest

def test_vic():
    vic_stream = Stream()
    print('\nLower house is live? ' + str(vic_stream.lower_is_live))
    print('Upper house is live? ' + str(vic_stream.upper_is_live))
    print('Committee is live? ' + str(vic_stream.committee_is_live))
    print(vic_stream.lower_stream_url)
    print(vic_stream.upper_stream_url)
    print(vic_stream.committee_stream_url)