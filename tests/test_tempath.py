import os
import pytest
import tempath


@pytest.mark.parametrize("size", [20, 280000, 25, 10000000])
def test_basicconfig(size):
    tempath.basicconfig(root_dir=None, min_file_size=None, max_file_size=size)
    if tempath.Register.config["max_file_size"] != size:
        raise AssertionError


def test_tempdir1():
    path = tempath.temp1()
    if not os.path.exists(path):
        raise AssertionError


def test_tempdir2():
    path = tempath.temp2()
    if not os.path.exists(path):
        raise AssertionError


def test_tempdir3():
    path = tempath.temp3()
    if not os.path.exists(path):
        raise AssertionError


def test_tempdir4():
    path = tempath.temp4()
    if not os.path.exists(path):
        raise AssertionError
