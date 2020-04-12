import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
import config
import pytest
from unittest import mock
from unittest.mock import patch, MagicMock

from libpycoder.atscraper import *

class TestAtScraper:
    def test_extract_task_screen_name(self):
        pass
    def test_extract_csrf_token(self):
        pass
    def test_extract_prob_links(self):
        pass