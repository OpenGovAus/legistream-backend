import re
from typing import List


from legistream_backend import StreamExtractor
from legistream_backend.util.models import StreamModel


class QLDStreamExtractor(StreamExtractor):

    BASE = 'https://tv.parliament.qld.gov.au'

    @property
    def extractor_name(self):
        return 'QLD'

    @property
    def streams(self) -> List[StreamModel]:
        return self._get_streams()

    def _get_streams(self) -> List[StreamModel]:
        homepage = self._download_html(self.BASE)

        if re.search(r'IsBroadcasting=True', str(homepage)):
            # TODO change this bit so it uses the JSON endpoint,
            # which is more accurate.
            is_live = True
            watch_page = self._download_html(
                f'{self.BASE}/TV/PartialGetHomeContent?'
                f'IsBroadcasting=True&Reference='
            )
            search = re.search(
                r"{ 'file': '(https?:\/\/[aA-zZ0-9\-\.\/]+"
                r"@[0-9/aA-zZ]+\.m3u8)",
                str(watch_page))

            if search:
                stream_url = search.group(1)

                stream_title = self._parse_cal(
                    f'{self.BASE}/TV/PartialCalendar') \
                    .replace('House Sitting Date', 'Legislative Assembly')
            else:
                is_live = False
                stream_url = ''
                stream_title = ''

        else:
            is_live = False
            stream_url = ''
            stream_title = ''

        if stream_title == 'Legislative Assembly':
            thumb = 'qld_la.webp'
        else:
            thumb = 'qld_generic.webp'

        model = StreamModel(
            url=stream_url,
            is_live=is_live,
            title=stream_title,
            thumb=thumb
        )

        return [model]

    def _parse_cal(self, url: str) -> str:
        page = self._download_html(url)
        most_recent = page.find_all(
            'div', {'class': 'row latest-posts-classic pad5B'})[-1] \
            .find('h3').text
        return most_recent
