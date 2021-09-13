import os
import pytest
from tempath import autodir, autofile


@pytest.fixture
def ten():
    return 10

def test_ten(ten):
    assert ten > 5

def test_autodir():
    fd = autodir()
    assert os.path.exists(fd)

def test_autofile_filecount():
    fd = autodir(folders=0, files=2)
    size = len(os.listdir(fd))
    assert size == 2

def test_ten(ten):
    assert ten > 5

def test_autofile():
    fd = autofile()
    assert os.path.exists(fd)

def test_autofile_size_10():
    kb = 1 << 10
    fd = autofile(size=kb)
    size = os.path.getsize(fd)
    assert size == kb

def test_autofile_size_16():
    kb = 1 << 16
    fd = autofile(size=kb)
    size = os.path.getsize(fd)
    assert size == kb

def test_autofile_size_1M():
    kb = 1 << 20
    fd = autofile(size=kb)
    size = os.path.getsize(fd)
    assert size == kb
