import pytest
import imagehash
from legistream_backend.tas import Stream

def test_img_hashes():
    tas_stream = Stream()
    if(isinstance(tas_stream.lower_img_hash, imagehash.ImageHash)):
        print('\n' + str(tas_stream.lower_img_hash))
    else:
        raise Exception('Lower image hash was not a valid ImageHash object.')

    if(isinstance(tas_stream.upper_img_hash, imagehash.ImageHash)):
        print(tas_stream.upper_img_hash)
    else:
        raise Exception('Upper image hash was not a valid ImageHash object.')

def test_stream_status():
    tas_stream = Stream()
    print('\nLower house "live" status: ' + str(tas_stream.lower_is_live))
    print('Upper house "live" status: ' + str(tas_stream.upper_is_live))
    print('\n' + str(tas_stream.stream_urls))

def test_stream_urls():
    tas_stream = Stream()
    print('\nLower M3U8 playlist: ' + tas_stream.lower_stream_url)
    print('Upper M3U8 playlist: ' + tas_stream.upper_stream_url)