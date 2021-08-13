import os
import os.path as path


def check_tempdir(dirpath):
    if not path.exists(path.realpath(dirpath)):
        if not path.exists(path.dirname(path.realpath(dirpath))):
            os.mkdir(path.dirname(path.realpath(dirpath)))
        else:
            os.mkdir(path.realpath(dirpath))
