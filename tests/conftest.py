import pytest
import sys
from unittest.mock import Mock

sys.modules['config'] = Mock()
import config

@pytest.fixture(scope="session", autouse=True)
def setup_config():
    """
    config.pyのモック処理
    """
    config.PASSWORD = ''
    config.USERNAME = ''
    config.ATCODER_DIR_PATH = '/Users/hoge/atcoder/'
    yield
