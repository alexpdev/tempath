import os
import pytest
import tempath


@pytest.mark.parametrize("size", [20, 280000, 25, 10000000])
def test_basicconfig(size):
    tempath.basicconfig(root_dir=None, min_file_size=None, max_file_size=size)
    assert tempath.Register.config["max_file_size"] == size


def test_tempdir1():
    path = tempath.temp1()
    assert os.path.exists(path)


def test_tempdir2():
    path = tempath.temp2()
    assert os.path.exists(path)


def test_tempdir3():
    path = tempath.temp3()
    assert os.path.exists(path)


def test_tempdir4():
    path = tempath.temp4()
    assert os.path.exists(path)
