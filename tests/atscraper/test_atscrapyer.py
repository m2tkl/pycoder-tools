import sys, os
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
import config
import pytest
from unittest import mock
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup as bs

from libpycoder.atscraper import *
from libpycoder import atscraper

class TestAtScraper:
    def test_extract_task_screen_name(self, monkeypatch):
        mock_prob_links = {
            'a': '/contests/abc123/tasks/abc123_a',
            'b': '/contests/abc123/tasks/abc123_b',
            'c': '/contests/abc123/tasks/abc123_c',
            'd': '/contests/abc123/tasks/abc123_d',
            'e': '/contests/abc123/tasks/abc123_e',
            'f': '/contests/abc123/tasks/abc123_f',
        }
        monkeypatch.setattr(atscraper,
                            'extract_prob_links',
                            lambda x: mock_prob_links)
        task = 'c'
        expected = 'abc123_c'
        test_src_path = ''.join([os.path.dirname(__file__),
                                 '/sources/tasks.html',])
        with open(test_src_path, 'r') as f:
            html = f.read()
        actual = extract_task_screen_name(html, task)
        assert actual == expected

    def test_extract_csrf_token(self):
        test_src_path = ''.join([os.path.dirname(__file__),
                                 '/sources/csrf.html',])
        with open(test_src_path, 'r') as f:
            html = f.read()
        expected = 'test_val_csrf_token'
        actual = extract_csrf_token(html)
        assert actual == expected

    def test_extract_prob_links(self):
        test_src_path = ''.join([os.path.dirname(__file__),
                                 '/sources/tasks.html',])
        with open(test_src_path, 'r') as f:
            html = f.read()
        expected = {
            'a': '/contests/abc123/tasks/abc123_a',
            'b': '/contests/abc123/tasks/abc123_b',
            'c': '/contests/abc123/tasks/abc123_c',
            'd': '/contests/abc123/tasks/abc123_d',
            'e': '/contests/abc123/tasks/abc123_e',
            'f': '/contests/abc123/tasks/abc123_f',
        }
        actual = extract_prob_links(html)
        assert actual == expected