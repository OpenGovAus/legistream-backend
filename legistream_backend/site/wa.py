from typing import List
from legistream_backend import StreamExtractor
from legistream_backend.util.models import StreamModel


class WAStreamExtractor(StreamExtractor):

    @property
    def extractor_name(self):
        return 'WA'

    @property
    def streams(self) -> List[StreamModel]:
        return self._get_streams()

    def _get_streams(self) -> List[StreamModel]:
        BRIGHTCOVE_API = 'https://edge.api.brightcove.com/playback/v1/acco' \
            'unts/6193427228001/videos/'
        ASSEMBLY = 'assembly'
        COUNCIL = 'council'
        COMMITTEE = 'committee'
        houses = {
            ASSEMBLY: 'Legislative Assembly',
            COUNCIL: 'Legislative Council'
        }
        thumbs = {
            ASSEMBLY: 'wa_la.webp',
            COUNCIL: 'wa_lc.webp',
            COMMITTEE: 'wa_com.webp'
        }
        streams_list = []
        for stream_page in [ASSEMBLY, COUNCIL]:
            page_url = f'https://{stream_page}linq.parliament.wa.gov.au/'
            dummy = StreamModel(
                    url='',
                    is_live=False,
                    title=houses[stream_page],
                    thumb=thumbs[stream_page]
                )
            landing = self._download_html(
                f'https://{stream_page}linq.parliament.wa.gov.au/')
            try:
                viewstate = {
                    '__EVENTVALIDATION': landing.find(
                        'input', {'name': '__EVENTVALIDATION'})['value'],

                    '__EVENTTARGET': 'ctl00$PlaceHolderMain$VideoButton',

                    '__VIEWSTATEGENERATOR': landing.find(
                        'input', {'name': '__VIEWSTATEGENERATOR'})['value'],
                    '__EVENTARGUMENT': '',

                    '__VIEWSTATE': landing.find(
                        'input', {'name': '__VIEWSTATE'})['value']
                }
                redir_url = self._download_page(
                    page_url,
                    method='POST',
                    postdata=viewstate
                ).url
                if redir_url == page_url:
                    streams_list.append(dummy)
                else:
                    watch_page = self._download_html(redir_url)
                    brightcove_id = watch_page.find(
                        'video-js')['data-video-id']
                    stream_api = self._download_json(
                        BRIGHTCOVE_API + brightcove_id, headers={
                            'Accept': 'application/json;pk=BCpkADawqM2ekcVYLH'
                                      'OvfmPvdxxol_QHum36qVcEDQmI8Hp5YIFuOoyZ'
                                      'jY8gmRg8B6TJEvX-KueK6KTlLjxw9xKJ4V-9UD'
                                      '1LAuRtCZ5tBdigaZxoq39BEqe2MWzkMOdVs1wr'
                                      'NANvIqKM8-H6'
                        })
                    stream_url = stream_api['sources'][0]['src']
                    streams_list.append(StreamModel(
                        url=stream_url,
                        is_live=True,
                        title=houses[stream_page],
                        thumb=thumbs[stream_page]
                    ))

            except Exception as e:
                print(f'Could not find VIEWSTATE info for '
                      f'{stream_page}\n\n{str(e)}')
                streams_list.append(dummy)

        return streams_list
