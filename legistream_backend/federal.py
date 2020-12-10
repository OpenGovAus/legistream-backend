import json
from requests import get
from bs4 import BeautifulSoup

refer_url = 'https://api-v3.switchmedia.asia/'
api_url = [refer_url + '277/assets/get-data?asset=11725', '&detail=verbose&format=json']
stream_base_url = 'https://dps-live-hls.global.ssl.fastly.net/hls/'
num_range = range(68, 71)
page_soup = BeautifulSoup(get('https://www.aph.gov.au/Watch_Read_Listen').text, 'lxml')

class Stream(object):
    def __init__(self):
        self.__get_stream_urls()
    
    def __get_stream_urls(self):
        self.sittings = []
        self.sitting_div = page_soup.find('div', {'id': 'content'}).find_all('p', {'class': 'watch-live text-center'})
        for row in self.sitting_div:
            self.sittings.append(row.text.strip())
        for asset_id in num_range:
            json_data = json.loads(get(api_url[0] + str(asset_id) + api_url[1]).text)[0]
            prefix_id = json_data['image'].replace('https://downloads.switchmedia.asia/filestore/getimage.php?siteID=', '')[:3]
            # prefix_id = '277'
            stream_id = json_data['title'][-3:]
            house_id = json_data['synopsis'].replace('Live Stream: ', '')[:3]
            url_suffix = prefix_id + '_' + house_id + stream_id + '_18000_01.m3u8'
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
        if(self.sittings[0] == 'Not sitting'):
           return(False)
        else:
           return(True)
        
    @property
    def upper_is_live(self):
        if(self.sittings[2] == 'Not sitting'):
           return(False)
        else:
           return(True)
    
    @property
    def committee_is_live(self):
        if(self.sittings[1] == 'Not sitting'):
           return(False)
        else:
           return(True)
    
    @property
    def stream_urls(self):
        return {'lower': self.lower_stream_url, 'upper': self.upper_stream_url, 'committee': self.committee_stream_url}