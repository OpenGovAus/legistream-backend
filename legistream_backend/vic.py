import m3u8
from requests import get

streams = ['https://pov_broadcast-i.akamaihd.net/hls/live/250374/pov-desk-la/master_900.m3u8',
           'https://pov_broadcast-i.akamaihd.net/hls/live/250376/pov-desk-lc/master_900.m3u8',
           'https://pov_broadcast-i.akamaihd.net/hls/live/250375/pov-desk-comm/master_900.m3u8']

class Stream(object):
    @property
    def lower_stream_url(self):
        return(streams[0])

    @property
    def upper_stream_url(self):
        return(streams[1])
    
    @property
    def committee_stream_url(self):
        return(streams[2])

    @property
    def stream_urls(self):
        return({'lower': self.lower_stream_url, 'upper': self.upper_stream_url, 'committee': self.committee_stream_url})

    @property
    def lower_is_live(self):
        if(get(self.lower_stream_url[:-15] + 'master_400.m3u8').status_code == 404):
            return False
        else:
            return True
        
    @property
    def upper_is_live(self):
        if(get(self.lower_stream_url[:-15] + 'master_400.m3u8').status_code == 404):
            return False
        else:
            return True
        
    @property
    def committee_is_live(self):
        if(get(self.committee_stream_url[:-15] + 'master_400.m3u8').status_code == 404):
            return False
        else:
            return True