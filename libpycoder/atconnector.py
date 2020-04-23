import requests
import sys
from .atscraper import extract_task_screen_name
from .atscraper import extract_csrf_token
from .atscraper import extract_prob_links
from .langs import get_lang_ids
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
        self.is_login = False

    def init_session(self) -> None:
        """セッションをログイン済の状態にする.
        config.pyにusername, passwordがなければログインしない.
        なお,ログインしていないとコードの提出ができず,
        開催中のコンテストではサンプルケースの取得ができない.
        """
        self.session = requests.session()
        if USERNAME is None or PASSWORD is None:
            return None
        csrf_token = self.get_csrf_token(LOGIN_URL)
        login_info = {"csrf_token": csrf_token,
                      "username": USERNAME,
                      "password": PASSWORD}
        res = self.post(LOGIN_URL, data=login_info)
        if res.status_code == 200:
            print("Login success!")
            self.is_login = True
        else:
            print("Login failed...")
            exit(1)

    def get_csrf_token(self, url):
        res = self.session.get(url)
        res.raise_for_status()
        html = res.text
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
        tasks_url = self._get_tasks_url(contest_type, contest_id)
        res = self.get(tasks_url)
        html = res.text
        return html

    def _get_tasks_url(self, contest_type, contest_id):
        return CONTEST_URL + contest_type + contest_id + '/tasks'

    def _get_submit_url(self, contest_type, contest_id):
        return CONTEST_URL + contest_type + contest_id + '/submit'

    def submit(self, contest_type, contest_id, prob_type, src, lang_type):
        if not self.is_login:
            print('Cannot submit because you are not logged in...')
            exit(1)
        submit_url = self._get_submit_url(contest_type, contest_id)
        csrf_token = self.get_csrf_token(submit_url)
        task_screen_name = self.get_task_screen_name(contest_type,
                                                     contest_id,
                                                     prob_type)
        lang_ids = get_lang_ids(lang_type)
        for lang_id in lang_ids:
            submit_info = {"data.TaskScreenName": task_screen_name,
                           "csrf_token": csrf_token,
                           "data.LanguageId": lang_id,
                           "sourceCode": src}
            try:
                res = self.post(submit_url, data=submit_info)
                res.raise_for_status()
                # raise_for_status()によって例外が早出されなければ
                # 提出できたということで終了
                break
            except requests.exceptions.HTTPError:
                # 例外が発生した場合は別のidで提出を試みる
                continue
        if res.status_code == 200:
            print('Submit!')
        else:
            print('cannot submit...')
            exit(1)
