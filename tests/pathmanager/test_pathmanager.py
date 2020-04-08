import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
import config
import pytest
from unittest import mock
from unittest.mock import patch, MagicMock

from libpycoder.pathmanager import PathManager

root_path = '/Users/hoge/atcoder/'

class TestPathManager:
    root_path = '/Users/hoge/atcoder/'

    def test_set_atcoder_dir_path_no_config(self, setup_obj):
        """
        config.pyにatcoderディレクトリの設定がない場合、
        カレントディレクトリをatcoderディレクトリとする
        """
        root_path = None
        pm = setup_obj
        pm._set_atcoder_dir_path(root_path)
        actual = pm.ATCODER_DIR
        expected = './ABC/123/'
        assert actual == expected

    def test_get_atcoder_dir_path_with_confing_path(self, setup_obj):
        """
        config.pyにatcoderディレクトリの設定がある場合、
        指定されたディレクトリを使用する
        """
        root_path = '/Users/hoge/atcoder/'
        pm = setup_obj
        pm._set_atcoder_dir_path(root_path)
        actual = pm.ATCODER_DIR
        expected = root_path + 'ABC/123/'
        assert actual == expected

    def test_get_prob_url(self, setup_obj):
        pm = setup_obj
        prob_type = 'a'
        actual = pm.get_prob_url(prob_type)
        expected = 'https://atcoder.jp/contests/abc123/tasks/abc123_' + prob_type
        assert actual == expected

    def test_get_submit_url(self, setup_obj):
        pm = setup_obj
        actual = pm.get_submit_url()
        expected = 'https://atcoder.jp/contests/abc123/submit'
        assert actual == expected

    def test_get_prob_file_path(self, setup_obj):
        pm = setup_obj
        prob_type = 'a'
        actual = pm.get_prob_file_path(prob_type)
        expected = root_path + 'ABC/123/' + 'A' + '.py'
        assert actual == expected

    def test_get_dir_path(self, setup_obj):
        prob_type = 'a'
        pm = setup_obj
        actual = pm.get_tests_dir_path(prob_type)
        expected = root_path + 'ABC/123/' + 'tests/' + 'A' + '/'
        assert actual == expected
