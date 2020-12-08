import m3u8, json
from requests import get
from bs4 import BeautifulSoup

MASTER_URL = 'http://dcunilive30-lh.akamaihd.net/i/dclive_1@535498/master.m3u8'
CALENDAR_URL = 'http://tv.parliament.qld.gov.au/TV/PartialCalendar'

class Stream(object):
    @property
    def is_live(self):
        try:
            self.m3u8_data = m3u8.parse(get(MASTER_URL).text)
            return True
        except:
            return False

    @property
    def stream_url(self):
        if(self.is_live):
            return(self.m3u8_data['playlists'][-1]['uri'])
        else:
            return ''

    @property
    def stream_title(self):
        if(self.is_live):
            soup = BeautifulSoup(get(CALENDAR_URL).text, 'lxml')
            try:
                return(soup.find_all('h3')[-1].text.strip())
            except:
                return ''

    @property
    def stream_urls(self):
        if(self.is_live):
            return {self.stream_title: self.stream_url}

print(Stream().stream_title)