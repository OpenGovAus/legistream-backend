from typing import List


from legistream_backend import StreamExtractor
from legistream_backend.util.models import StreamModel


class ACTStreamExtractor(StreamExtractor):

    @property
    def extractor_name(self):
        return 'ACT'

    @property
    def streams(self) -> List[StreamModel]:
        return self._get_streams()

    def _get_streams(self) -> List[StreamModel]:
        api_return = self._download_json(
            'https://aod.parliament.act.gov.au/api/video',
            verify=False)['live']

        url = api_return['url'] + api_return['extension']
        m3u8_return = self._download_m3u8(url, verify=False)

        is_live = False
        if len(m3u8_return['playlists']) > 0:
            is_live = True

        model = StreamModel(
            url=url,
            is_live=is_live,
            title='Legislative Assembly',
            thumb='act_la.webp'
        )

        return [model]
