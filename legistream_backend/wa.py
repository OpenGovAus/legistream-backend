from typing import Text
import m3u8
import urllib3
from bs4 import BeautifulSoup
from requests import get

urllib3.disable_warnings()

lower_master = 'https://streamer1.parliament.wa.gov.au/live/smil:AssemblyLinqStream.smil/playlist.m3u8'
upper_master = 'https://streamer2.parliament.wa.gov.au/live/smil:CouncilLinqStream.smil/playlist.m3u8'
stream_page_url = 'https://parliament.wa.gov.au/WebCMS/webcms.nsf/watch-live'

class Stream(object):
    @property
    def lower_is_live(self):
        try:
            box = BeautifulSoup(get(stream_page_url, verify=False).text, 'lxml').find('div', {'class': 'watchbox la'})
            heading = box.find('h6', string='Nothing Scheduled')
            if(heading):
                return False
            else:
                return True
        except:
            return False

    @property
    def upper_is_live(self):
        try:
            box = BeautifulSoup(get(stream_page_url, verify=False).text, 'lxml').find('div', {'class': 'watchbox lc'})
            heading = box.find('h6', string='Nothing Scheduled')
            if(heading):
                return False
            else:
                return True
        except:
            return False

    @property
    def lower_stream_url(self):
        if(self.lower_is_live):
            return('https://streamer1.parliament.wa.gov.au/live/smil:AssemblyLinqStream.smil/' + self.__get_playlist(lower_master))
        else:
            return ''

    @property
    def upper_stream_url(self):
        if(self.upper_is_live):
            return('https://streamer2.parliament.wa.gov.au/live/smil:CouncilLinqStream.smil/' + self.__get_playlist(upper_master))
        else:
            return ''

    @property
    def stream_urls(self):
        return({'lower': self.lower_stream_url, 'upper': self.upper_stream_url})

    def __get_playlist(self, input_url):
        dat = m3u8.parse(get(input_url, verify=False).text)
        return(dat['playlists'][0]['uri'])