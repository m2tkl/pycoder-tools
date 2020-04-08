import pytest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from libpycoder.pathmanager import PathManager
import config

@pytest.fixture(scope='function', autouse=True)
def setup_obj():
    print('\nsetup before module')
    pm = PathManager('abc', '123')
    yield pm
    print('\nsetup after module')
