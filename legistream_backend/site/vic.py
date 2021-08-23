from typing import List
from datetime import datetime
from requests import head


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
                if head(stream_url).status_code == 200:
                    master = self._download_m3u8(stream_url)
                    try:
                        playlists = master['playlists'][0]['uri']
                        master_playlist = stream_url.replace(
                            'master.m3u8', playlists
                        )
                        is_live = True if head(master_playlist).status_code \
                            == 200 else False
                    except Exception:
                        is_live = False

                streams_list.append(StreamModel(
                    url=stream_url,
                    thumb=thumbnail,
                    is_live=is_live,
                    title=stream_title
                ))

        return streams_list
