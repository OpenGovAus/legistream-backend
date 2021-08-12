from typing import List
from requests import get


from legistream_backend import StreamExtractor
from legistream_backend.util.models import StreamModel


class StreamExtractor(StreamExtractor):

    PREFIX = 'https://player-api.new.livestream.com/accounts/13067949/events/'

    @property
    def are_streams(self):
        casts = self._download_html(
            'https://www.parliament.nsw.gov.au/Pages/webcasts.aspx') \
                .find('div', {'class': 'webcast-links'}).text.strip()
        if casts == 'There are no active webcasts, on sitting days see ' \
                    'the Daily Program to determine when proceedings begin.':
            return False
        else:
            return True

    @property
    def extractor_name(self):
        return 'NSW'

    @property
    def streams(self) -> List[StreamModel]:
        return self._get_streams()

    def _get_streams(self) -> List[StreamModel]:
        api_res = self._download_json(self.PREFIX)['data']

        streams_list = []
        for stream in api_res:
            stream_data = self._download_json(
                self.PREFIX + str(stream['id']) + '/stream_info')

            stream_title = stream['full_name']

            try:
                stream_data['name']
                stream_url = ''  # When a playlist is present, the "name" key is not present.
                is_live = False
            except Exception:
                stream_url = get(stream_data['secure_m3u8_url'],
                                 allow_redirects=True).url
                is_live = True

            if stream_title in ['Jubilee Room', 'Macquarie Room'] and is_live:
                is_live = False

            model = StreamModel(
                url=stream_url,
                is_live=is_live,
                title=stream_title
            )

            streams_list.append(model)

        return streams_list
