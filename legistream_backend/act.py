import m3u8, json
from requests import get

api_url = 'http://aod.parliament.act.gov.au/api/video'

class Stream(object):
    __api_call = json.loads(get(api_url).text)['live']

    @property
    def lower_stream_url(self):
        return self.__api_call['url'] + self.__api_call['extension']
    
    @property
    def lower_is_live(self):
        if(m3u8.parse(get(self.lower_stream_url).text)['playlists']):
            return True
        else:
            return False
    
    @property
    def stream_urls(self):
        return {'lower': self.lower_stream_url}