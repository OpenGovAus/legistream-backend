import sys

operating_system = sys.platform

if(operating_system != 'win32'):
    root_dir = '/tmp/.legistream/'
    ffmpeg_bin = 'ffmpeg'
else:
    root_dir = 'C:/temp/.legistream/'
    ffmpeg_bin = 'ffmpeg.exe'
