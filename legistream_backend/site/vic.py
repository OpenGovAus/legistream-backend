from typing import List
from datetime import datetime

from requests import get


from legistream_backend import StreamExtractor
from legistream_backend.util.models import StreamModel


BASE = 'https://www.parliament.vic.gov.au'


class VICStreamExtractor(StreamExtractor):

    @property
    def extractor_name(self):
        return 'Victoria'

    @property
    def streams(self) -> List[StreamModel]:
        return self._get_streams()

    def _get_streams(self) -> List[StreamModel]:
        timestamp = int(datetime.now().timestamp())
        api_json = self._download_json(f'{BASE}/video-streaming/v7/scripts/ak'
                                       f'amai_desktop.json?_={timestamp}')
        streams_list = []
        if len(api_json) > 0:
            for stream in api_json:
                stream_title = stream['title'].replace(' - Desktop', '')

                if 'Council' in stream_title:
                    thumbnail = 'vic_lc.webp'
                elif 'Assembly' in stream_title:
                    thumbnail = 'vic_la.webp'
                else:
                    thumbnail = 'vic_com.webp'

                stream_url = 'https:' + stream['source'][0]['src']
                is_live = True if get(stream_url).status_code == 200 else False
                streams_list.append(StreamModel(
                    url=stream_url,
                    thumb=thumbnail,
                    is_live=is_live,
                    title=stream_title
                ))

        return streams_list
