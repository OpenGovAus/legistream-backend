import os
import m3u8
import subprocess
import imagehash
import shutil

from PIL import Image
from requests import get
from bs4 import BeautifulSoup
from datetime import datetime

from legistream_backend import common
from legistream_backend.util.fileutils import check_tempdir


filepath = os.path.dirname(os.path.realpath(__file__))

class Stream(object):
    lower_img_hash = 18446744069414592512
    upper_img_hash = 18446743326385257472
    
    @property
    def lower_stream_url(self):
        return BeautifulSoup(get('https://www.parliament.tas.gov.au/TBS/havideo.html').text, 'lxml').find('source')['src']

    @property
    def upper_stream_url(self):
        return BeautifulSoup(get('https://www.parliament.tas.gov.au/TBS/LCvideo.html').text, 'lxml').find('source')['src']

    @property
    def stream_urls(self):
        return({'lower': self.lower_stream_url, 'upper': self.upper_stream_url})


    @property
    def lower_is_live(self):
        try:
            if(abs(self.lower_img_hash - self.__get_vid_hash(self.lower_stream_url)) < 16385):
                return(False)
            else:
                return(True)
        except Exception:
            return False
        
    @property
    def upper_is_live(self):
        if(abs(self.upper_img_hash - self.__get_vid_hash(self.upper_stream_url)) < 16385):
            return(False)
        else:
            return(True)

    def __cleanup(self, directory): # Clear Legistream's temp directory
        try:
            if(os.path.exists(directory)):
                shutil.rmtree(directory)
        except Exception as e:
            print(e)

    def __get_vid_hash(self, input_url):
        check_tempdir(common.root_dir)
        try:
            playlist_data = m3u8.loads(get(input_url).text)
        except Exception:
            return None
        seg_uri = m3u8.loads(get(input_url.replace('playlist.m3u8', '') + playlist_data.data['playlists'][0]['uri']).text).data['segments'][-1]['uri']
        seg_ts = get(input_url.replace('playlist.m3u8', '') + seg_uri)
        current_time = str(datetime.now()).replace(':', '-').replace('.', '-').replace(' ', '_')

        seg_output_file = common.root_dir + current_time + '_tas_seg.ts'
        with open(seg_output_file, 'wb') as file:
            file.write(seg_ts.content)
        
        img_out = common.root_dir + current_time + '_tas_seg_out.jpg'
        
        command = ['-ss', '00:00:00', '-i', seg_output_file, '-frames:v', '1', img_out]
        subprocess.run([common.ffmpeg_bin] + command, capture_output=True)
        _hash = int(str(imagehash.average_hash((Image.open(img_out)))), 16)
        self.__cleanup(common.root_dir)
        return _hash