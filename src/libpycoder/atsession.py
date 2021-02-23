import requests
import sys
import pickle
import datetime
import os
from getpass import getpass
from . import atscraper

LOGIN_URL = 'https://atcoder.jp/login'
CONTEST_URL = 'https://atcoder.jp/contests/'


class AtSession:
    """AtCoderとのセッションを管理する
    """

    def __init__(self):
        self.session = requests.session()
        self.is_login = False
        self.max_sesison_time = 30*60
        self.session_file = './session.dump'
        self.load_cache()

    def login(self):
        """login to a session.
        cacheファイルにログイン済みセッションが保存されている場合は再利用する.
        cacheファイルが古い場合は再度ログインを求められる.
        """
        use_cache = self.load_cache()
        if use_cache:
            self.is_login = self.check_status()
        else:
            # 有効なキャッシュがなければ新しくsessionを作る
            self._init_session()
            self._save_session_to_cache()
        if not self.is_login:
            self._init_session()
            self._save_session_to_cache()

    def logout(self):
        if os.path.exists(self.session_file):
            os.remove(self.session_file)
            print('Logout')
        else:
            print('Already logout.')

    def _init_session(self):
        self.session = requests.session()
        username = input('username: ')
        password = getpass('password: ')
        csrf_token = self.get_csrf_token(LOGIN_URL)
        login_info = {'csrf_token': csrf_token,
                      'username': username,
                      'password': password}
        res = self.session.post(LOGIN_URL, login_info, allow_redirects=False)
        # リダイレクト先が '/login' でなければログイン成功
        if res.headers['location'] != '/login':
            print('Login success!')
            self.is_login = True
        else:
            print('Login failed...')
            exit(1)

    def _save_session_to_cache(self):
        with open(self.session_file, 'wb') as f:
            pickle.dump(self.session, f)

    def _modification_date(self, filename):
        t = os.path.getmtime(filename)
        return datetime.datetime.fromtimestamp(t)

    def get_csrf_token(self, url: str) -> str:
        """csrfトークンを取得する.
        :param url: csrfトークンを取得したいページのurl
        :return csrf_token: csrfトークン
        """
        res = self.session.get(url)
        res.raise_for_status()
        html = res.text
        csrf_token = atscraper.extract_csrf_token(html)
        return csrf_token

    def post(self, url, data=None):
        res = self.session.post(url, data)
        # update session cache
        self._save_session_to_cache()
        return res

    def get(self, url):
        res = self.session.get(url)
        # update session cache
        self._save_session_to_cache()
        return res

    def check_status(self) -> bool:
        print('[login status]: ', end='')
        # 有効なcacheがない場合はlogin失敗
        use_cache = self.load_cache()
        if not use_cache:
            print('NG')
            print("Please login. Use 'pycoder login'")
            return False
        # 提出ページにアクセスできるかどうかで判定
        url = CONTEST_URL + 'abc001/submit'
        res = self.session.get(url, allow_redirects=False)
        if res.status_code != 302:
            print('OK')
            return True
        else:
            print('NG')
            print("Please login. Use 'pycoder login'")
            return False

    def load_cache(self) -> bool:
        """sessionのcacheを読み込む.
        cacheの最終更新からの経過時間がmax_session_timeで
        指定されている期間を超えていた場合は読み込まない
        :return use_cashe: cacheを使用した場合はTrue, そうでなければFalse
        """
        use_cache = False
        if os.path.exists(self.session_file):
            last_modified = self._modification_date(self.session_file)
            elapsed_time = (datetime.datetime.now() - last_modified).seconds
            if elapsed_time < self.max_sesison_time:
                with open(self.session_file, 'rb') as f:
                    self.session = pickle.load(f)
                    use_cache = True
        return use_cache
