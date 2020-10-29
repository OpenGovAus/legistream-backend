import m3u8
from requests import get

api_url = 'http://video.dpa.act.gov.au/live/amlst:aod-recording/playlist.m3u8?DVR'

class Stream(object):
    def __init__(self):
        self.__read_playlist(api_url)
    
    def __read_playlist(self, input_url):
        playlist_data = m3u8.loads(get(input_url).text)
        self.lower_stream_url = 'http://video.dpa.act.gov.au/live/amlst:aod-recording/' + playlist_data.data['playlists'][2]['uri']
        self.stream_urls = {'lower': self.lower_stream_url}

    @property
    def lower_is_live(self):
        if(get(self.lower_stream_url).status_code == 404):
            return(False)
        else:
            return(True)