import sys
import pytest
from unittest.mock import patch
import requests
from requests import Session

from libpycoder.atsession import AtSession
from libpycoder import atsession

class MockResponse:
    def __init__(self, status_code, text=None):
        self.status_code = status_code
        self.text = text

class TestAtSession:

    @patch.object(Session, 'post', return_value=MockResponse(200))
    def test_post(self, mock_response):
        AS = AtSession()
        AS.session = requests.session()
        res = AS.post('test_url')
        assert res.status_code == 200