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

def _getline(length=63):
    phrase = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    return phrase[:length]

def fillfile(path, size=16384, random=False):
    total = 0
    if random:
        line = _randline()
    else:
        line = _getline()
    linelen = len(line)
    with open(path, "wb") as fd:
        while total + linelen < size:
            fd.write(line)
            total += linelen
        fd.write(line[:size-total])
    return fd

def autofile(size=16384, random=False):
    tempfile = os.path.join(Reg.path,"testfile.tmp")
    fillfile(tempfile, size=size, random=random)
    Reg.include(tempfile)
    return tempfile

def filldir(path, count=1, size=16384, random=False):
    Reg.include(path)
    for i in range(count):
        name = f"testfile_{i}.tmp"
        full = os.path.join(path, name)
        fillfile(full, size=size, random=random)
    return

def autodir(folders=0,files=2,size=16384,random=False):
    tempdir = os.path.join(Reg.path, "test_folder")
    Reg.include(tempdir)
    for i in range(folders):
        testdir = os.path.join(tempdir, f"testdir{i}")
        filldir(testdir, count=files, size=size, random=random)
    filldir(tempdir, count=files, size=size, random=random)
    return tempdir

@atexit.register
def cleanup():
    list(map(rmpath, Reg.paths))
    Reg.clean()
