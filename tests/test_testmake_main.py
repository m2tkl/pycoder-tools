import pytest
import sys
from pathlib import Path
from unittest.mock import patch
sys.path.append(str(Path(__file__).resolve().parent.parent))
from libpycoder.testmake import TestMaker
import pycode

@pytest.mark.skip(reason='pytestskip')
@patch.object(TestMaker, 'fetch_sample_cases', return_value=0)
def test_fetch_sample_cases(mock_func):
    sys.argv.append('abc')
    sys.argv.append('123')
    pycode.main()
    mock_func.assert_called_once_with()

@pytest.mark.skip(reason='pytestskip')
def test_add_test_case():
    pass
