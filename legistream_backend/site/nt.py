import re
import m3u8
from typing import List
from requests import get


from legistream_backend import StreamExtractor
from legistream_backend.util.models import StreamModel


class StreamExtractor(StreamExtractor):

    @property
    def extractor_name(self):
        return 'NT'

    @property
    def streams(self) -> List[StreamModel]:
        return self._get_streams()

    def _get_streams(self) -> List[StreamModel]:
        stream_page = self._download_page(
            'https://parliament.nt.gov.au/about/broadcast/video-broadcast',
            verify=False)

        stream_url = re.search(
            r"videoSource = '(https[:/aA-zZ0-9\.]+)", stream_page).group(1)

        stream_segments = stream_segments = m3u8.parse(
            self._download_page(stream_url))['segments']

        seg_lens = []
        for i in range(3):
            seg_lens.append(len(get(
                stream_url.replace(
                    'playlist.m3u8', '') + stream_segments[-(i + 1)]['uri']).content))

        if(any(seg_lens.count(element) > 1 for element in seg_lens)):
            is_live = False
        else:
            is_live = True

        model = StreamModel(
            url=stream_url.replace('SD', 'HD'),
            is_live=is_live,
            title='Legislative Assembly'
        )

        return [model]
