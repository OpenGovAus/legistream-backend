import datetime
from typing import List


from legistream_backend import StreamExtractor
from legistream_backend.util.models import StreamModel


BASE = 'https://aod.parliament.act.gov.au/'


class ACTStreamExtractor(StreamExtractor):

    @property
    def extractor_name(self):
        return 'ACT'

    @property
    def streams(self) -> List[StreamModel]:
        return self._get_streams()

    def _get_streams(self) -> List[StreamModel]:
        api_return = self._download_json(
            BASE + 'api/video',
            verify=False)['live']

        url = api_return['url'] + api_return['extension']

        stream_title = 'Legislative Assembly'
        is_live = False
        sitting_types = ['session', 'hearing']
        date_timestamp = int(self._get_timestamp(
            str(datetime.date.today()), '%Y-%m-%d'))
        for sitting_type in sitting_types:
            sitting_data = self._download_json(
                BASE + f'api/{sitting_type}/next')
            for date in sitting_data:
                timestamp = int(self._get_timestamp(date['date'], '%Y-%m-%d'))
                if timestamp == date_timestamp:
                    is_live = True
                    if len(date['description']) > 0:
                        stream_title = date['description']

        model = StreamModel(
            url=url,
            is_live=is_live,
            title=stream_title,
            thumb='act_la.webp'
        )

        return [model]
