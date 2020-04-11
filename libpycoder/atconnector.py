import requests
import sys
from .atscraper import extract_task_screen_name
from .atscraper import extract_csrf_token
from .atscraper import extract_prob_links
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import config

ATCODER_URL = 'https://atcoder.jp'
LOGIN_URL = 'https://atcoder.jp/login'
CONTEST_URL = 'https://atcoder.jp/contests/'
USERNAME = config.USERNAME
PASSWORD = config.PASSWORD

class AtConnector:
    def __init__(self):
        self.session = None

    def login(self):
        # セッション開始
        self.session = requests.session()
        # csrf_token取得
        csrf_token = self.get_csrf_token(LOGIN_URL)
        # パラメータセット
        login_info = {"csrf_token": csrf_token,
                      "username": USERNAME,
                      "password": PASSWORD}
        res = self.post(LOGIN_URL, data=login_info)
        res.raise_for_status()
        if res.status_code == 200: print("Login success!")
        else: print("Login failed..."); exit(1)

    def get_csrf_token(self, url):
        html = self.session.get(url)
        html.raise_for_status()
        csrf_token = extract_csrf_token(html)
        return csrf_token

    def post(self, url, data=None):
        res = self.session.post(url, data)
        return res

    def get(self, url):
        return self.session.get(url)

    def get_task_screen_name(self, contest_type, contest_id, prob_type):
        html = self._get_contest_tasks_page(contest_type, contest_id)
        task_screen_name = extract_task_screen_name(html, prob_type)
        return task_screen_name

    def get_prob_urls(self, contest_type, contest_id):
        """コンテスト問題一覧ページから各問題のurlを取得して返す
        Args:
            contest_type: abc, arc, agc, ...
            contest_id: 123, ...
        Returns:
            prob_links: 各問題へのurlを持つ辞書
        """
        html = self._get_contest_tasks_page(contest_type, contest_id)
        prob_links = extract_prob_links(html)
        for prob_type, link in prob_links.items():
            prob_links[prob_type] = ATCODER_URL + link
        return prob_links

    def _get_contest_tasks_page(self, contest_type, contest_id):
        tasks_url = CONTEST_URL + contest_type + contest_id + '/tasks'
        html = self.get(tasks_url)
        return html

if __name__ == '__main__':
    ac = AtConnector()
    ac.login()
