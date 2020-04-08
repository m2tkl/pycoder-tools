import sys, os
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
import config

class PathManager:
    CONTEST_URL = 'https://atcoder.jp/contests/'
    SUBMIT_URL  = ''
    ATCODER_DIR = ''

    def __init__(self, contest_type, contest_id):
        self.contest_type = contest_type
        self.contest_id = contest_id

        PathManager.SUBMIT_URL = \
            PathManager.CONTEST_URL + contest_type + contest_id + '/submit'

        self._set_atcoder_dir_path(config.ATCODER_DIR_PATH)

    def _set_atcoder_dir_path(self, root_path):
        res = ''
        if not root_path == None:
            res = root_path
        else:
            res = './'
        res += self.contest_type.upper() + '/' + self.contest_id + '/'
        PathManager.ATCODER_DIR = res

    def get_prob_url(self, prob_type):
        prob_url = \
            PathManager.CONTEST_URL + self.contest_type + self.contest_id \
            + '/tasks/' \
            + self.contest_type + self.contest_id + '_' + prob_type
        return prob_url

    def get_submit_url(self):
        return PathManager.SUBMIT_URL

    def get_prob_file_path(self, prob_type):
        file_path = PathManager.ATCODER_DIR + prob_type.upper() + '.py'
        return file_path

    def get_tests_dir_path(self, prob_type):
        tests_path = PathManager.ATCODER_DIR + 'tests/' + prob_type.upper() + '/'
        return tests_path

