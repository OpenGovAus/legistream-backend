import json
import m3u8
import http.cookiejar
from requests import get

api_url = ['https://api-v3.switchmedia.asia/277/assets/get-data?asset=11725', '&detail=verbose&format=json']
stream_base_url = 'https://dps-live-hls.global.ssl.fastly.net/hls/'
refer_url = 'https://api-v3.switchmedia.asia/'
num_range = range(68, 71)

headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
    'Referer': 'https://api-v3.switchmedia.asia/switch.tv/vcms/wrapper.html.php?videoID=1172568&siteID=277&autoplay=true',
    'Host': 'dps-live-hls.global.ssl.fastly.net',
    'Sec-Fetch-Site': 'cross-site',
    'Connection': 'keep-alive',
    'Accept-Language': 'en-AU,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': '*/*'
}

# print(json.dumps(headers, indent=2))

class Stream(object):
    def __init__(self):
        self.__get_stream_urls()
    
    def __get_stream_urls(self):
        for asset_id in num_range:
            json_data = json.loads(get(api_url[0] + str(asset_id) + api_url[1]).text)[0]
            prefix_id = json_data['image'].replace('https://downloads.switchmedia.asia/filestore/getimage.php?siteID=', '')[:3]
            # prefix_id = '277'
            stream_id = json_data['title'][-3:]
            house_id = json_data['synopsis'].replace('Live Stream: ', '')[:3]
            url_suffix = prefix_id + '_' + house_id + '_' + stream_id + '_1800_01.m3u8'
            url = stream_base_url + url_suffix
            if(house_id == 'HOR'):
                self.lower_stream_url = url
            elif(house_id == 'COM'):
                self.committee_stream_url = url
            elif(house_id == 'SEN'):
                self.upper_stream_url = url
            else:
                raise Exception('An error occurred, got house_id ' + str(house_id))

    @property
    def lower_is_live(self):
        stat = get(self.lower_stream_url, headers=headers)
        print(json.dumps(dict(stat.headers), indent=2))
        #if(stat.strip()[-22:] == '#EXT-X-MEDIA-SEQUENCE:'):
         #   return(False)
        #else:
         #   return(True)