import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from libpycoder.langs import *

lang_ids = {
    'python': [3023, 4006],
    'pypy': [3510, 4047],
}

class TestLangs:
    def test_get_python_ids(self):
        expected = lang_ids['python']
        actual = get_lang_ids('p')
        assert actual == expected

    def test_get_pypy_ids(self):
        expected = lang_ids['pypy']
        actual = get_lang_ids('pp')
        assert actual == expected

    def test_get_none_ids(self):
        expected = None
        actual = get_lang_ids('hoge')
        assert actual == expected