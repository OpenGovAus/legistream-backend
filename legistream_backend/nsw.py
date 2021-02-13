import json, m3u8
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
        playlist_uri = m3u8.parse(get(self.committe_stream_url).text)['playlists'][0]['uri']
        segments= m3u8.parse(get(playlist_uri).text)['segments']
        base_url = playlist_uri.split('/media')[0]
        seg_lens = []
        for i in range(4):
            seg_lens.append(len(get(segments[-(i + 1)]['uri'].replace('..', base_url)).content))
        if(all(elem in [511360, 510608, 510420, 511736, 510232, 510984, 510044, 510796, 511736, 509856, 511172, 511548]  for elem in seg_lens)):
            return False
        else:
            print(seg_lens)
            return True

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