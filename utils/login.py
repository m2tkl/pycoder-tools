import requests
from bs4 import BeautifulSoup
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import config

LOGIN_URL = 'https://atcoder.jp/login'
USERNAME = config.USERNAME
PASSWORD = config.PASSWORD

class AtConnector():
    def __init__(self):
        self.session = None

    def login(self):
        # セッション開始
        self.session = requests.session()
        # csrf_token取得
        r = self.session.get(LOGIN_URL)
        s = BeautifulSoup(r.text, 'lxml')
        csrf_token = s.find(attrs={'name': 'csrf_token'}).get('value')
        # パラメータセット
        login_info = {"csrf_token": csrf_token,
                      "username": USERNAME,
                      "password": PASSWORD}
        result = self.session.post(LOGIN_URL, data=login_info)
        result.raise_for_status()
        if result.status_code==200:
            print("Login success!")
        else:
            print("Login failed...")
            exit(1)


if __name__ == '__main__':
    ac = AtConnector()
    ac.login()
