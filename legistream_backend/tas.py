import subprocess

from requests import get

base_stream_url = 'https://5ea8aa5cf299b.streamlock.net/'

class Stream(object):
    def __init__(self):
        self.lower_stream_url = base_stream_url + 'HA/house_360p/playlist.m3u8'
        self.upper_stream_url = base_stream_url + 'LC/legco_360p/playlist.m3u8'
        self.stream_urls = {'lower': self.lower_stream_url, 'upper': self.upper_stream_url}

    @property
    def lower_is_live(self):
        self.__dl_video(self.lower_stream_url)
        
    def __dl_video(self, input_url):
        pass