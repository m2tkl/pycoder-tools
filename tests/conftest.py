import pytest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
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
