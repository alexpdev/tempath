import pytest


@pytest.fixture
def dirtest():
    return 10

def test_autodir(dirtest):
    assert dirtest > 5
