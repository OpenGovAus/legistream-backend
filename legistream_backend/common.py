import sys

operating_system = sys.platform

if(operating_system != 'win32'):
    root_dir = '/tmp/'
    ffmpeg_bin = 'ffmpeg'
else:
    root_dir = 'C:/temp/'
    ffmpeg_bin = 'ffmpeg.exe'