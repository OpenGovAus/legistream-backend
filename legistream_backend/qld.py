import m3u8, json, re
from requests import get
from bs4 import BeautifulSoup

CALENDAR_URL = 'http://tv.parliament.qld.gov.au/TV/PartialCalendar'

class Stream(object):
    @property
    def is_live(self):
        try:
            self.m3u8_data = m3u8.parse(get(self.stream_url).text)
            if(self.m3u8_data['playlists']):
                return True
            else:
                return False
        except:
            return False

    @property
    def stream_url(self):
        _js = BeautifulSoup(get('http://tv.parliament.qld.gov.au/TV/PartialGetHomeContent').text, 'lxml').find('script').string.split('\n')
        
        for index,line in enumerate(_js):
            if(line.strip() == 'var videoSources = ['):
                try:
                    return json.loads(_js[index + 1].replace('];', '').replace(',', '').strip().replace("'", '"'))['file']
                except:
                    return ''

    @property
    def stream_title(self):
        if(self.is_live):
            soup = BeautifulSoup(get(CALENDAR_URL).text, 'lxml')
            try:
                _title = soup.find_all('h3')[-1].text.strip()
                if(_title == 'House Sitting Date'):
                    return 'Legislative Assembly'
                else:
                    return _title
            except:
                return ''
        else:
            return ''

    @property
    def stream_urls(self):
        if(self.is_live):
            return {self.stream_title: self.stream_url}
        else:
            return {}