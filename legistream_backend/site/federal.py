import re
from typing import List


from legistream_backend import StreamExtractor
from legistream_backend.util.models import StreamModel


class FEDERALStreamExtractor(StreamExtractor):

    @property
    def extractor_name(self):
        return 'Federal'

    BASE_URL = 'https://www.aph.gov.au'

    @property
    def streams(self) -> List[StreamModel]:
        return self._get_streams()

    def _get_streams(self) -> List[StreamModel]:
        final_list = []
        homepage = self._download_html(
            f'{self.BASE_URL}/Watch_Read_Listen')
        for stream_row in homepage.find(
                            'section', {'id': 't1-content-panel'}).find_all(
                            'div', {'class': 'row border-top'}):

            try:
                info_block = stream_row.find(
                    'div', {'class': 'medium-7 columns'}).find('a')
            except Exception:
                final_list.append(StreamModel(
                    url='',
                    is_live=False,
                    title='',
                    thumb=''
                ))
                continue

            stream_title = info_block.contents[0].strip()

            stream_page_url = re.search(
                r"window\.open\(\'([&aA-zZ0-9\-/\?={}]+)",
                info_block['onclick']).group(1)

            video_id = re.search(r'videoID=([0-9]+)', self._download_html(
                f'{self.BASE_URL}{stream_page_url}')
                    .find('iframe', {'title': 'Media player'})['src']).group(1)

            stream_url = self._download_json(
                f'https://api-v3.switchmedia.asia/277/playback/'
                f'getUniversalPlayerConfig?videoID={video_id}&format=json')[
                    'media']['renditions'][0]['url']

            if stream_title == 'House of Representatives':
                thumb = 'fed_hor.webp'
            elif stream_title == 'Senate':
                thumb = 'fed_sen.webp'
            else:
                thumb = 'fed_placeholder.webp'

            model = StreamModel(
                url=stream_url,
                is_live=True,
                title=stream_title,
                thumb=thumb
            )
            final_list.append(model)

        return final_list
