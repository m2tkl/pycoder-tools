import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
import config
import pytest
from unittest.mock import patch
import requests
from requests import Session

from libpycoder.atconnector import AtConnector
from libpycoder import atconnector

class MockResponse:
    def __init__(self, status_code, text=None):
        self.status_code = status_code
        self.text = text

class TestAtConnector:

    @pytest.mark.skip(reason='pytestskip')
    @patch.object(Session, 'post', return_value=MockResponse(200))
    def test_post(self, mock_response):
        ac = AtConnector()
        ac.session = requests.session()
        res = ac.post('test_url')
        assert res.status_code == 200

    @pytest.mark.skip(reason='pytestskip')
    @patch.object(Session, 'get', return_value=MockResponse(200, text='test'))
    def test_get(self, mock_response):
        ac = AtConnector()
        ac.session = requests.session()
        res = ac.get('test_url')
        assert res.status_code == 200
        assert res.text == 'test'

    # login処理はatsessionに移行
    @pytest.mark.skip(reason='pytestskip')
    @patch.object(Session, 'post', return_value=MockResponse(200))
    @patch.object(AtConnector, 'get_csrf_token', return_value='')
    def test_init_atconnector_login_success(self, mock_response, func_mock):
        ac = AtConnector()
        assert ac.session == None
        assert ac.is_login == False
        ac.init_session()
        assert ac.session != None
        assert ac.is_login == True

    # login処理はatsessionに移行
    @pytest.mark.skip(reason='pytestskip')
    @patch.object(Session, 'post', return_value=MockResponse(400))
    @patch.object(AtConnector, 'get_csrf_token', return_value='')
    def test_init_atconnector_login_failed(self, mock_response, func_mock):
        ac = AtConnector()
        assert ac.session == None
        assert ac.is_login == False
        with pytest.raises(SystemExit):
            ac.init_session()
        assert ac.session != None
        assert ac.is_login == False

    def test_get_tasks_url_normal_contest(self):
        ac = AtConnector()
        actual = ac._get_tasks_url('abc', '123')
        expected = 'https://atcoder.jp/contests/abc123/tasks'
        assert actual == expected

    def test_get_tasks_url_other_contest(self):
        ac = AtConnector()
        actual = ac._get_tasks_url('others', 'hoge-con')
        expected = 'https://atcoder.jp/contests/hoge-con/tasks'
        assert actual == expected

    def test_get_submit_url_normal_contest(self):
        ac = AtConnector()
        actual = ac._get_submit_url('abc', '123')
        expected = 'https://atcoder.jp/contests/abc123/submit'
        assert actual == expected

    def test_get_submit_url_other_contest(self):
        ac = AtConnector()
        actual = ac._get_submit_url('others', 'hoge-con')
        expected = 'https://atcoder.jp/contests/hoge-con/submit'
        assert actual == expected

    def test_get_submission_result_url_for_normal_contest(self):
        ac = AtConnector()
        actual = ac._get_submission_result_url('abc', '123')
        expected = 'https://atcoder.jp/contests/abc123/submissions/me'
        assert actual == expected

    def test_get_submission_result_url_for_other_contest(self):
        ac = AtConnector()
        actual = ac._get_submission_result_url('others', 'hoge-con')
        expected = 'https://atcoder.jp/contests/hoge-con/submissions/me'
        assert actual == expected

    @patch.object(Session, 'get', return_value=MockResponse(200, text='ttext'))
    def test_get_contest_tasks_page(self, mock_response):
        ac = AtConnector()
        ac.session = requests.session()
        actual = ac._get_contest_tasks_page('abc','123')
        assert actual == 'ttext'