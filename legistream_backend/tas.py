import io
import os
import sys
import m3u8
import subprocess
import imagehash
from PIL import Image
from datetime import datetime
from requests import get

operating_system = sys.platform

filepath = os.path.dirname(os.path.realpath(__file__))

base_stream_url = 'https://5ea8aa5cf299b.streamlock.net/'
lower_base_url = 'HA/house_360p/'
upper_base_url = 'LC/legco_360p/'

class Stream(object):
    lower_img_hash = imagehash.average_hash(Image.open(filepath + '/tas_img/ha_adjourned.png'))
    upper_img_hash = imagehash.average_hash(Image.open(filepath + '/tas_img/lc_adjourned.png'))
    def __init__(self):
        self.lower_stream_url = base_stream_url + lower_base_url + 'playlist.m3u8'
        self.upper_stream_url = base_stream_url + upper_base_url + 'playlist.m3u8'
        self.stream_urls = {'lower': self.lower_stream_url, 'upper': self.upper_stream_url}

    @property
    def lower_is_live(self):
        if(self.lower_img_hash - self.__get_vid_hash(self.lower_stream_url, lower_base_url) < 5):
            return(False)
        else:
            return(True)
        
    @property
    def upper_is_live(self):
        if(self.upper_img_hash - self.__get_vid_hash(self.upper_stream_url, upper_base_url) < 5):
            return(False)
        else:
            return(True)

    def __get_vid_hash(self, input_url, base_url):
        try:
            if(operating_system != 'win32'):
                root_dir = '/tmp/'
            else:
                root_dir = 'C:/temp/'
            playlist_data = m3u8.loads(get(input_url).text)
            seg_uri = m3u8.loads(get(base_stream_url + base_url + playlist_data.data['playlists'][0]['uri']).text).data['segments'][-1]['uri']
            seg_ts = get(base_stream_url + base_url + seg_uri)
            current_time = str(datetime.now()).replace(':', '-').replace('.', '-').replace(' ', '_')
            seg_output_file = root_dir + current_time + '_seg.ts'
            open(seg_output_file, 'wb').write(seg_ts.content)
            img_out = root_dir + current_time + '_seg_out.png'
            
            command = ['-ss', '00:00:00', '-i', seg_output_file, '-frames:v', '1', img_out]
            if(operating_system != 'win32'):
                subprocess.run(['ffmpeg'] + command, capture_output=True)
            else:
                subprocess.run(['ffmpeg.exe'] + command, capture_output=True)
            
            return(imagehash.average_hash((Image.open(img_out))))
        except:
            raise Exception('Invalid input URL: ' + input_url)