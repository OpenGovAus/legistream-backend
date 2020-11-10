import m3u8
import json
from requests import get

data_json = 'https://player-api.new.livestream.com/accounts/13067949/events/'
info_suffix = '/stream_info'

class Stream(object):
    def __init__(self):
        try:
            self.__get_data(data_json)
        except:
            raise Exception('Unable to get JSON data: ' + data_json)

    def __get_data(self, input_json):
        self.parsed_data = json.loads(get(input_json).text)['data']
    
    @property
    def lower_stream_url(self):
        return(self.__get_stream_url('Legislative Assembly'))

    @property
    def upper_stream_url(self):
        return(self.__get_stream_url('Legislative Council'))
    
    @property
    def committe_stream_url(self):
        return(self.__get_stream_url('Macquarie Room'))
    
    @property
    def jubilee_stream_url(self):
        return(self.__get_stream_url('Jubilee Room'))

    @property
    def jubilee_is_live(self):
        try:
            get(self.jubilee_stream_url)
            return(True)
        except:
            return(False)

    @property
    def committee_is_live(self):
        try:
            get(self.committe_stream_url)
            return(True)
        except:
            return(False)
        
    @property
    def lower_is_live(self):
        try:
            get(self.lower_stream_url)
            return(True)
        except:
            return(False)
        
    @property
    def upper_is_live(self):
        try:
            get(self.upper_stream_url)
            return(True)
        except:
            return(False)

    @property
    def stream_urls(self):
        return({'lower': self.lower_stream_url, 'upper': self.upper_stream_url, 'committee': self.committe_stream_url, 'jubilee': self.jubilee_stream_url})

    def __get_stream_url(self, input_title):
        for stream in self.parsed_data:
            if(input_title == stream['full_name']):
                stream_id = str(stream['id'])
                stream_json_data = json.loads(get(data_json + stream_id + info_suffix).text)
                try:
                    stream_json_data['name']
                    return ''
                except:
                    res = get(stream_json_data['secure_m3u8_url'], allow_redirects=True)
                    return res.url

print(Stream().lower_stream_url)