import m3u8
from requests import get

stream_url = 'https://pbs1.nt.gov.au/HLS/SDPull/playlist.m3u8'

class Stream(object):
    @property
    def lower_is_live(self):
        try:
            raw_m3u8 = get(stream_url).text
            return True
        except:
            return False

    @property
    def lower_stream_urls(self):
        if(self.lower_is_live):
            playlist_data = m3u8.parse(get(stream_url).text)
            # I can't code the rest of this until the NT goes live

print(Stream().lower_is_live)