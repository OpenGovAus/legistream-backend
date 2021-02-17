import m3u8, json
from requests import get

base = 'http://pbs1.nt.gov.au/HLS/HDPull/'
stream_url = base + 'playlist.m3u8'

class Stream(object):
    @property
    def lower_is_live(self):
        stream_segments = m3u8.parse(get(stream_url).text)['segments']
        seg_lens = []
        for i in range(3):
            seg_lens.append(len(get(base + stream_segments[-(i + 1)]['uri']).content))
        if(any(seg_lens.count(element) > 1 for element in seg_lens)):
            return False
        else:
            return True
    
    @property
    def lower_stream_url(self):
        return stream_url

    @property
    def stream_urls(self):
        return({'lower': self.lower_stream_url})