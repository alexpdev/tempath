import os
import shutil
import atexit
import random
import string

class TempFileError(Exception):
    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Register:

    def __init__(self):
        self.paths = []
        if not os.path.exists("TempFolder"):
            os.mkdir("TempFolder")
        self.path = os.path.abspath("TempFolder")

    def include(self, path):
        if not os.path.exists(path):
            os.mkdir(path)
        self.paths.append(path)

    def clean(self):
        rmpath(self.path)

Reg = Register()


def rmpath(path):
    if os.path.exists(path):
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
        else:
            raise TempFileError(f"Cannot interperet {path}.")

def _randline(length=63):
    choices = string.printable + string.whitespace
    line = "".join([random.choice(choices) for _ in range(length)]) + "\n"
    return line.encode("utf-8")

def fillfile(path, size=16384):
    total = 0
    line = _randline()
    linelen = len(line)
    with open(path, "wb") as fd:
        while total + linelen < size:
            fd.write(line)
            total += linelen
        fd.write(line[:size-total])
    return fd

def autofile(size=16384):
    tempfile = os.path.join(Reg.path,"testfile.tmp")
    fillfile(tempfile, size=size)
    Reg.include(tempfile)
    return tempfile

def filldir(path, count=1):
    Reg.include(path)
    for i in range(count):
        name = f"testfile_{i}.tmp"
        full = os.path.join(path, name)
        fillfile(full)
    return

def autodir(folders=0,files=2):
    tempdir = os.path.join(Reg.path, "test_folder")
    Reg.include(tempdir)
    for i in range(folders):
        testdir = os.path.join(tempdir, f"testdir{i}")
        filldir(testdir,count=files)
    filldir(tempdir, count=files)
    return tempdir

@atexit.register
def cleanup():
    list(map(rmpath, Reg.paths))
    Reg.clean()
