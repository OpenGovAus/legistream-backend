import m3u8
import json
import urllib3
from requests import get

urllib3.disable_warnings()

lower_master = 'https://streamer1.parliament.wa.gov.au/live/smil:AssemblyLinqStream.smil/playlist.m3u8'
upper_master = 'https://streamer2.parliament.wa.gov.au/live/smil:CouncilLinqStream.smil/playlist.m3u8'

class Stream(object):
    @property
    def lower_is_live(self):
        try:
            with get(lower_master, verify=False) as res:
                if(res.status_code != 200):
                    return False
                else:
                    return True
        except:
            return False

    @property
    def upper_is_live(self):
        try:
            with get(upper_master, verify=False) as res:
                if(res.status_code != 200):
                    return False
                else:
                    return True
        except:
            return False

    @property
    def lower_stream_url(self):
        if(self.lower_is_live):
            return('https://streamer1.parliament.wa.gov.au/live/smil:AssemblyLinqStream.smil/' + self.__get_playlist(lower_master))

    @property
    def upper_stream_url(self):
        if(self.upper_is_live):
            return('https://streamer2.parliament.wa.gov.au/live/smil:CouncilLinqStream.smil/' + self.__get_playlist(upper_master))

    @property
    def stream_urls(self):
        return({'lower': self.lower_stream_url, 'upper': self.upper_stream_url})

    def __get_playlist(self, input_url):
        dat = m3u8.parse(get(input_url, verify=False).text)
        return(dat['playlists'][0]['uri'])