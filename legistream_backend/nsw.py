import json, m3u8
from requests import get
from bs4 import BeautifulSoup

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
    def are_streams(self):
        _html = BeautifulSoup(get('https://www.parliament.nsw.gov.au/Pages/webcasts.aspx').text, 'lxml').find('div', {'class': 'webcast-links'})
        try:
            if(_html.find('p').text == 'There are no active webcasts, on sitting days see the Daily Program to determine when proceedings begin.'):
                return False
            else:
                return True
        except:
            return True


    @property
    def lower_stream_url(self):
        return(self.__get_stream_url('Legislative Assembly'))

    @property
    def upper_stream_url(self):
        return(self.__get_stream_url('Legislative Council'))
    
    @property
    def committee_stream_url(self):
        return(self.__get_stream_url('Macquarie Room'))
    
    @property
    def jubilee_stream_url(self):
        return(self.__get_stream_url('Jubilee Room'))

    @property
    def jubilee_is_live(self):
        try:
            if(self.are_streams and get(self.jubilee_stream_url).status_code == 200):
                return True
            else:
                return False
        except:
            return False

    @property
    def committee_is_live(self):
        try:
            if(self.are_streams and get(self.committee_stream_url).status_code == 200):
                return True
            else:
                return False
        except:
            return False

    @property
    def lower_is_live(self):
        try:
            get(self.lower_stream_url)
            return True
        except:
            return False
        
    @property
    def upper_is_live(self):
        try:
            get(self.upper_stream_url)
            return True
        except:
            return False

    @property
    def stream_urls(self):
        return({'lower': self.lower_stream_url, 'upper': self.upper_stream_url, 'committee': self.committee_stream_url, 'jubilee': self.jubilee_stream_url})

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