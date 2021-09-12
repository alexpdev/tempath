import os
import atexit
import shutil
import random
import string
from pathlib import Path

__version__ = "0.1.0"
__author__ = "alexpdev"

__all__ = ["autofile", "autodir"]

class TempFileError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

def rmpath(path):
    if os.path.exists(path):
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
    raise TempFileError(f"Cannot interperet {path}.")

def fillfile(path, size=16384):
    line = _randline()
    total = linelen = len(line)
    with open(path, "wb") as fd:
        while True:
            if total + linelen < size:
                fd.write(line)
                total += linelen
                continue
            diff = abs(size - total)
            line = _randline(diff)
            fd.write(line)
            break
    return fd

def filldir(path, count=1):
    for i in range(count):
        name = f"testfile_{i}.tmp"
        full = os.path.join(path, name)
        fillfile(full)
    return

def autodir(folders=0,files=2):
    temp = _check_temp()
    tempdir = os.path.join(temp, "test_folder")
    for i in range(folders):
        testdir = os.path.join(tempdir, f"testdir{i}")
        filldir(testdir,count=files)
    filldir(tempdir)
    return tempdir

def autofile(size=16384):
    temp = _check_temp()
    tempfile = temp / "test_file.tmp"
    fillfile(tempfile, size=size)
    return tempfile

def _check_temp():
    if not os.path.exists("temp"):
        os.mkdir("temp")
    return Path("temp").resolve()


def _randline(length=80):
    choices = string.printable + string.whitespace
    line = "".join([random.choice(choices) for _ in range(length)])
    return line.encode("utf-8")

@atexit.register
def _autoremove():
    paths = map(lambda x: os.path.join("temp",x),"test_folder", "test_file.tmp")
    map(rmpath,paths)
