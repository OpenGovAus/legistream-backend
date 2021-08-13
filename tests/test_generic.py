import os
import re
import sys
import pytest
import importlib


from legistream_backend.util.models import StreamModel
from legistream_backend.util import url_re


@pytest.fixture()
def parliament(pytestconfig):
    return pytestconfig.getoption("parl")


@pytest.fixture
def parl_module(parliament):
    folder = os.path.dirname(
        os.path.dirname(os.path.realpath(__file__)))

    spec = importlib.util.spec_from_file_location(
        'parl', f'{folder}'
        f'/legistream_backend/site/{parliament}.py')

    parl = importlib.util.module_from_spec(spec)
    sys.modules['parl'] = parl
    spec.loader.exec_module(parl)
    return parl


def test_parliament(parl_module):
    '''The generic test uses importlib to dynamically import
       the parliament modules. Since all modules follow the
       same return template, the generic test works for all
       of them.
    '''
    ext_name = os.path.basename(
        os.path.splitext(parl_module.__file__)[0]).upper()
    exec(f'_extractor_obj = parl_module.{ext_name}StreamExtractor()')
    extractor_obj = locals()['_extractor_obj']
    stream_data = extractor_obj.streams
    print(stream_data)
    assert isinstance(stream_data, list)

    for index, stream in enumerate(stream_data):
        assert isinstance(stream, StreamModel)
        assert isinstance(stream.is_live, bool)
        assert isinstance(stream.title, str)

        if stream.is_live:
            assert isinstance(stream.url, str)
            assert re.match(url_re, stream.url)
            print(f'{extractor_obj.extractor_name} '
                  f'stream {index + 1} is live.\n\nURL:\n'
                  f'{stream.url}\n\nTitle:\n{stream.title}')
        else:
            print(f'{extractor_obj.extractor_name} stream '
                  f'{index + 1} is not live.')
