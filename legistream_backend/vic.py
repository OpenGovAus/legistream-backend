import m3u8, json, subprocess, imagehash, os
from PIL import Image
from requests import get
from datetime import datetime
from . import common

filepath = os.path.dirname(os.path.realpath(__file__))

upper_base_url = 'https://pov_broadcast-i.akamaihd.net/hls/live/250376/pov-desk-lc/'
lower_base_url = 'https://pov_broadcast-i.akamaihd.net/hls/live/250374/pov-desk-la/'
committee_base_url = 'https://pov_broadcast-i.akamaihd.net/hls/live/250375/pov-desk-comm/'
suffix = 'master_900.m3u8'

streams = [lower_base_url + suffix,
           upper_base_url + suffix,
           committee_base_url + suffix]

class Stream(object):
    lower_img_hash = imagehash.average_hash(Image.open(filepath + '/vic_img/la_adjourned.png'))
    upper_img_hash = imagehash.average_hash(Image.open(filepath + '/vic_img/lc_adjourned.png'))

    @property
    def lower_stream_url(self):
        return(streams[0])

    @property
    def upper_stream_url(self):
        return(streams[1])
    
    @property
    def committee_stream_url(self):
        return(streams[2])

    @property
    def stream_urls(self):
        return({'lower': self.lower_stream_url, 'upper': self.upper_stream_url, 'committee': self.committee_stream_url})

    @property
    def lower_is_live(self):
        if(self.lower_img_hash - self.__check_img(0) < 5):
            return False
        else:
            return True
        
    @property
    def upper_is_live(self):
        if(self.upper_img_hash - self.__check_img(1) < 5):
            return False
        else:
            return True
        
    @property
    def committee_is_live(self):
        if(get(self.committee_stream_url[:-15] + 'master_400.m3u8').status_code == 404):
            return False
        else:
            return True

    def __check_img(self, house):
        if(isinstance(house, int)):
            if(house == 0):
                base = lower_base_url
            elif(house == 1):
                base = upper_base_url
            elif(house == 2):
                base = committee_base_url
            else:
                raise Exception('Chamber value out of range (0 - 2)')
            seg = m3u8.parse(get(streams[house]).text)['segments'][-1]['uri']
            current_time = str(datetime.now()).replace(':', '-').replace('.', '-').replace(' ', '_')
            seg_output_file = common.root_dir + current_time + '_vic_seg.ts'
            with open(seg_output_file, 'wb') as file:
                file.write(get(base + seg).content)
            
            img_out = common.root_dir + current_time + '_vic_seg_out.png'
            
            command = ['-ss', '00:00:00', '-i', seg_output_file, '-frames:v', '1', img_out]
            subprocess.run([common.ffmpeg_bin] + command, capture_output=True)
            
            return(imagehash.average_hash((Image.open(img_out))))
        else:
            raise ValueError('house must be 0, 1, or 2.')