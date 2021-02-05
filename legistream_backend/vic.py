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
        return('https://pov_broadcast-I.akamaihd.net/hls/live/250374-b/pov-desk-la/' + m3u8.parse(get(f'https:{self.lower_stream()["altsrc"]}').text)['playlists'][-1]['uri'])

    @property
    def lower_is_live(self):
        if(get(self.lower_stream_url).status_code != 200):
            return False
        else:
            return True

    @property
    def upper_stream_url(self):
        return 'https://pov_broadcast-i.akamaihd.net/hls/live/250376-b/pov-desk-lc/' + m3u8.parse(get(f'https:{self.upper_stream()["altsrc"]}').text)['playlists'][-1]['uri']

    @property
    def upper_is_live(self):
        if(get(self.upper_stream_url).status_code != 200):
            return False
        else:
            return True

    @property
    def committee_stream_url(self):
        return('https://pov_broadcast-I.akamaihd.net/hls/live/250375/pov-desk-comm/' + m3u8.parse(get(f'https:{self.comm_stream()["source"][0]["src"]}').text)['playlists'][-1]['uri']) 

    @property
    def committee_is_live(self):
        if(get(self.committee_stream_url).status_code != 200):
            return False
        else:
            return True