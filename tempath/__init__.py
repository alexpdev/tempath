import os
import shutil
import atexit
import string
import random


__version__ = "0.1.5"
__author__ = "alexpdev"


def rmpath(path):
    if os.path.exists(path):
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
        if os.path.exists(path):
            return False
    return True


class Register:

    paths = []

    @classmethod
    def include(cls, path):
        if path not in cls.paths:
            cls.paths.append(path)

    @classmethod
    def clear(cls):
        for path in cls.paths:
            rmpath(path)


def reg(func):
    def wrapper(path, *args, **kwargs):
        Register.include(path)
        return func(path, *args, **kwargs)

    return wrapper


def basicconfig(max_file_size=None, min_file_size=None, root_dir=None):
    partials = []
    config = {
        "max_file_size": max_file_size,
        "min_file_size": min_file_size,
        "root_dir": root_dir,
    }
    if not root_dir:
        test = os.path.join(os.curdir, "test")
        if os.path.exists(test):
            root_dir = config["root_dir"] = os.path.join(test, "TEMPROOT")
        elif os.path.exists(test + "s"):
            root_dir = config["root_dir"] = os.path.join(test + "s", "TEMPROOT")
        else:
            root_dir = config["root_dir"] = os.path.join(os.curdir, "TEMPROOT")
    while not os.path.exists(root_dir):
        parent, base = os.path.split(root_dir)
        partials.insert(0, base)
        root_dir = parent
    for partial in partials:
        path = os.path.join(root_dir, partial)
        makedir(path)
        root_dir = path
    Register.config = config
    assert os.path.exists(config["root_dir"])


def config(func):
    def wrapper(*args, **kwargs):
        if not hasattr(Register, "config"):
            basicconfig()
        assert hasattr(Register, "config")
        return func(*args, **kwargs)

    return wrapper


def _fixedline():
    fixed = string.printable + string.hexdigits + string.whitespace
    return fixed.encode("utf-8")


@reg
def fillfile(path, size):
    line = _fixedline()
    size = size if size > 28 else 2 ** size
    with open(path, "wb") as fd:
        while size > 0:
            fd.write(line)
            size -= len(line)
    return path


@reg
def makedir(path):
    if os.path.exists(path):
        rmpath(path)
    os.mkdir(path)


def random_size():
    max_file = Register.config["max_file_size"]
    min_file = Register.config["min_file_size"]
    if not max_file or not min_file:
        if not max_file and not min_file:
            max_file = Register.config["max_file_size"] = 2 ** 28
            min_file = Register.config["min_file_size"] = 2 ** 13
        elif not max_file:
            if min_file > 28:
                max_file = Register.config["max_file_size"] = 2 ** 28
        elif not min_file:
            if max_file > 28:
                min_file = Register.config["min_file_size"] = 2 ** 13
    size = random.randint(min_file, max_file + 1)
    return size


def walk(structure, root):
    for k, v in structure.items():
        path = os.path.join(root, k)
        makedir(path)
        if isinstance(v, list):
            for file_d in v:
                dest = os.path.join(path, file_d)
                size = random_size()
                fillfile(dest, size)
        else:
            walk(v, path)


@config
def construct(base, structure):
    root = Register.config["root_dir"]
    path = os.path.join(root, base)
    if structure:
        makedir(path)
        walk(structure, path)
    else:
        size = random_size()
        fillfile(path, size)
    return path


def temp1():
    return construct("tempfile1", None)


def temp2():
    structure = {"dir1": {"dir2": ["file1", "file2"], "dir3": ["file3", "file4"]}}
    return construct("tempdir2", structure)


def temp3():
    structure = {"dir1": ["file1", "file2", "file3", "file4", "file5"]}
    return construct("temdir3", structure)


def temp4():
    structure = {"dir1": {"dir2": {"dir3": ["file1"]}}}
    return construct("tempdir4", structure)


@atexit.register
def cleanup():
    Register.clear()
