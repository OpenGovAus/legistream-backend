import m3u8, json
from requests import get
from requests.sessions import SessionRedirectMixin

API_URL = 'https://www.parliament.vic.gov.au/video-streaming/v7/scripts/akamai_desktop.json?_=1612478772960'

class Stream(object):
    def __init__(self):
        self.__get_api_data(API_URL)

    def __get_api_data(self, url):
        self.api_data = json.loads(get(url).text)
    
    def lower_stream(self):
        return self.__get_stream('Assembly Live Broadcast - Desktop')

    def upper_stream(self):
        return self.__get_stream('Council Live Broadcast - Desktop')

    def comm_stream(self):
        return self.__get_stream('Committee Live Broadcast - Desktop')

    def __get_stream(self, title):
        for stream in self.api_data:
            if(stream['title'] == title):
                return stream

    @property
    def lower_stream_url(self):
        return f'https:{self.lower_stream()["checksrc"]}'.replace('400', '900')

    @property
    def lower_is_live(self):
        if(get(self.lower_stream_url).status_code != 200):
            return False
        else:
            return True

    @property
    def upper_stream_url(self):
        return f'https:{self.upper_stream()["checksrc"]}'.replace('400', '900')

    @property
    def upper_is_live(self):
        if(get(self.upper_stream_url).status_code != 200):
            return False
        else:
            return True

    @property
    def committee_stream_url(self):
        try:
            return f'https:{self.comm_stream()["checksrc"]}'.replace('400', '900')
        except:
            return None

    @property
    def committee_is_live(self):
        try:
            if(get(self.committee_stream_url).status_code != 200):
                return False
            else:
                return True
        except:
            return False