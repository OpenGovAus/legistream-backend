from datetime import datetime
from typing import List


from legistream_backend import StreamExtractor
from legistream_backend.util.models import StreamModel


BASE = 'https://www.parliament.tas.gov.au'


class SittingCalendar(StreamExtractor):

    def __init__(self, homepage: str) -> None:
        self.url = homepage
        self.days = dict()
        for week in self._download_html(homepage).find(
            'table',
            {
                'id': 'calendar'
            }
        ).find_all('tr')[1:]:
            for index, day in enumerate(week.find_all('td')):
                day_dict = {
                    'lower': False,
                    'upper': False
                }
                try:
                    if day.has_attr('class'):
                        if day['class'] == ['Both']:
                            day_dict['lower'] = True
                            day_dict['upper'] = True
                        elif day['class'] == ['HA']:
                            day_dict['lower'] = True
                        elif day['class'] == ['LC']:
                            day_dict['upper'] = True
                        else:
                            raise ValueError('Unrecognised day type: '
                                             f'{day["class"]}.')
                    self.days[self.timestamp(day.text)] = day_dict
                except ValueError:
                    pass  # Blank text for this day

    def __str__(self):
        return f"<Parliament Calendar | URL: '{self.url}'>"

    def __repr__(self):
        return ('<{}.{} : {} object at {}>'.format(
            self.__class__.__module__,
            self.__class__.__name__,
            self.url,
            hex(id(self))))

    def timestamp(self, day):
        return self._get_timestamp(
            f'{day} {datetime.now().month} {datetime.now().year}',
            '%d %m %Y'
        )

    @property
    def all_days(self):
        return self.days

    @property
    def sitting_days(self):
        return [x for x in self.all_days.keys() if
                any(self.all_days[x].values())]


class TASStreamExtractor(StreamExtractor):

    @property
    def extractor_name(self) -> str:
        return 'Tasmania'

    @property
    def streams(self) -> List[StreamModel]:
        return self._get_streams()

    def detect_live(self, house: str, cal: SittingCalendar):
        assert isinstance(cal, SittingCalendar)
        time = datetime.now()
        today_timestamp = self._get_timestamp(
            f'{time.year} {time.month} {time.day}',
            '%Y %m %d'
        )
        return cal.all_days[today_timestamp][house]

    def _get_streams(self) -> List[StreamModel]:
        parl_calendar = SittingCalendar(BASE)
        cast_pages = ['havideo', 'LCvideo', 'com1tbs', 'com2tbs']
        STREAM_BASE = BASE + '/TBS/'

        streams_list = []
        for address in cast_pages:
            cast_url = f'{STREAM_BASE}{address}.html'
            page = self._download_html(cast_url).find('main')
            stream_title = page.find('h2').text.replace(
                'Parliament of Tasmania - ', '').replace(
                    ' Webcast', '').strip()
            if 'Committee' in stream_title:
                stream_thumb = 'tas_com.webp'
                stream_stat = False  # TODO get status of committee streams.
            elif 'Assembly' in stream_title:
                stream_thumb = 'tas_ha.webp'
                stream_stat = self.detect_live('lower', parl_calendar)
            elif 'Council' in stream_title:
                stream_thumb = 'tas_lc.webp'
                stream_stat = self.detect_live('upper', parl_calendar)
            else:
                raise ValueError('Could not detect thumbnail '
                                 f'for "{stream_title}".')
            stream_url = page.find('source')['src']
            streams_list.append(StreamModel(
                url=stream_url,
                is_live=stream_stat,
                title=stream_title,
                thumb=stream_thumb
            ))

        return streams_list
