import m3u8
import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup


requests.packages.urllib3.disable_warnings()


class StreamExtractor(object):

    def _download_page(self, url, postdata={}, method='GET', verify=True):
        if method == 'GET':
            return requests.get(url, verify=verify).text
        elif method == 'POST':
            return requests.post(url, data=postdata, verify=verify).text
        else:
            raise self.ExtractorError(
                "Invalid request method used, requires 'GET' or 'POST'")

    def _download_json(self, url, postdata={}, method='GET', verify=True):
        page_content = self._download_page(
            url, method=method, postdata=postdata, verify=verify)
        try:
            return json.loads(page_content)
        except Exception as e:
            raise self.ExtractorError('Could not encode JSON; ' + str(e))

    def _download_html(self, url, postdata={}, method='GET', verify=True):
        page_content = self._download_page(
            url, method=method, postdata=postdata, verify=verify)
        try:
            return BeautifulSoup(page_content, 'lxml')
        except Exception as e:
            raise self.ExtractorError(
                'Could not parse page with bs4; ' + str(e))

    def _download_m3u8(self, url, postdata={}, method='GET', verify=True):
        page_content = self._download_page(
            url, method=method, postdata=postdata, verify=verify)
        try:
            return m3u8.parse(page_content)
        except Exception as e:
            raise self.ExtractorError(
                'Could not parse response as M3U8 playlist; ' + str(e))

    def _get_timestamp(self, text, pattern):
        return int(datetime.strptime(text, pattern).timestamp())

    def _get_epoch(self):
        return int(datetime.now().timestamp())

    class ExtractorError(Exception):
        pass
