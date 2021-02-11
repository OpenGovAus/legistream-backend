import json, re
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
        self.__scrape_committees()

    def __scrape_committees(self):
        live_pages = []
        self.com_urls = []
        chk_list = BeautifulSoup(get('https://www.aph.gov.au/Watch_Read_Listen').text, 'lxml').find('section', {'id': 't1-content-panel'}).find_all('div', {'class': 'medium-7 columns'})
        for entry in chk_list:
            if(entry.text.strip()[-4:] == 'Live'):
                _stream_title = entry.text.strip()[:-4].strip()
                if(_stream_title == 'Senate' or _stream_title == 'House of Representatives' or _stream_title == 'Federation Chamber'):
                    pass
                else:
                    live_pages.append({'title': entry.text.strip()[:-4].strip(),'url': 'https://www.aph.gov.au' + entry.find('a')['onclick'][13:][:75]})
        if(not len(live_pages) == 0):
            for url in live_pages:
                try:
                    self.com_urls.append({'title': url['title'], 'url': json.loads(get('https://api-v3.switchmedia.asia/277/playback/getUniversalPlayerConfig?videoID=' + BeautifulSoup(get(url['url']).text, 'lxml').find('iframe')['src'][72:][:7] + '&playlistID=0&skinType=vcms&profile=regular&playerID=playerregular&format=json&bookmarkID=0&autoplay=true&referrer=https://www.aph.gov.au/News_and_Events/LiveMediaPlayer&siteID=277&cl=1').text)['media']['renditions'][0]['url']})
                except:
                    # This happens with audio-only streams, which Legistream doesn't support yet...
                    pass
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
            url_suffix = prefix_id + '_' + house_id + stream_id + '_18000.m3u8'
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
        if(self.sittings[1] == 'Not sitting' and not 'https://dps-live-hls.global.ssl.fastly.net/hls/277_COM109_18000.m3u8' in self.com_urls):
           return(False)
        else:
           return(True)
    
    @property
    def stream_urls(self):
        data_dict = {'lower': self.lower_stream_url, 'upper': self.upper_stream_url, 'committee': self.committee_stream_url, 'extra_committees': self.com_urls}
        for entry in data_dict:
            if(data_dict[entry] in data_dict['extra_committees']):
                data_dict['extra_committees'].remove(data_dict[entry])
        if(len(data_dict['extra_committees']) == 0):
            data_dict.pop('extra_committees', None)
        return data_dict