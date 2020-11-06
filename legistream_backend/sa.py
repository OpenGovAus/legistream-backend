import json
import random
import requests
from websocket import create_connection

lower_stream_id = '23181491'
upper_stream_id = '23195631'

rnd = random.randrange

def num_to_hex(n):
    return hex(n)[2:]

class Stream(object):
    @property
    def lower_is_live(self):
        return(self.__get_stream_status(lower_stream_id))

    @property
    def upper_is_live(self):
        return(self.__get_stream_status(upper_stream_id))

    @property
    def lower_stream_url(self):
        if(self.lower_is_live):
            return(self.__get_stream_json(lower_stream_id)['streamFormats'])
        else:
            return ''

    @property
    def upper_stream_url(self):
        if(self.upper_is_live):
            return(self.__get_stream_json(upper_stream_id)['streamFormats'])
        else:
            return ''

    @property
    def stream_urls(self):
        return({'lower': self.lower_stream_url, 'upper': self.upper_stream_url})

    def __get_stream_status(self, stream_id):
        return(bool(self.__get_stream_json(stream_id)['contentAvailable']))
        

    def __get_stream_json(self, stream_id):
        ws = create_connection('wss://r%d-1-%s-channel-wss-omega.ums.ustream.tv/1/ustream' % (rnd(1e8), stream_id), header=['User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'], origin='https://www.ustream.tv')
        args = {
            'type': 'viewer',
            'appId': 3,
            'appVersion': 2,
            'application': 'channel',
            'buildNumber': "2.26.7",
            'clusterHost': "r%d-1-%s-channel-omega.ums.services.video.ibm.com" % (rnd(1e8), stream_id),
            'rsid': '%s:%s' % (num_to_hex(rnd(1e8)), num_to_hex(rnd(1e8))),
            'rpin': '_rpin.%d' % rnd(1e15),
            'referrer': 'https://www.parliament.sa.gov.au/',
            'media': stream_id
        }
        ws.send(json.dumps({'cmd': 'connect', 'args': [args]}))
        stream_dat = json.loads(ws.recv())
        return(stream_dat['args'][0]['stream'])