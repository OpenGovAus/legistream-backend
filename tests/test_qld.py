import pytest
from legistream_backend.qld import Stream

qld_stream = Stream()

def test_qld_status():
    print('\nQLD Parliament stream status: %s.' % (str(qld_stream.is_live)))

def test_qld_stream_url():
    print('\nQLD Parliament stream url: %s.' % (qld_stream.stream_url))

def test_qld_stream_title():
    print('\nMost recent QLD stream title: %s.' % (qld_stream.stream_title))

def test_qld_stream_urls():
    print('\n%s' % (qld_stream.stream_urls))