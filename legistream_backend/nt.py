from requests import get

stream_url = 'http://pbs1.nt.gov.au/HLS/HDPull/playlist.m3u8'

class Stream(object):
    @property
    def lower_is_live(self):
        try:
            get(stream_url)
            return True
        except:
            return False

    @property
    def lower_stream_url(self):
        if(self.lower_is_live):
            return stream_url
        else:
            return ''

    @property
    def stream_urls(self):
        return({'lower': self.lower_stream_url})