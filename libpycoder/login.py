import requests
from bs4 import BeautifulSoup as bs
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import config

LOGIN_URL = 'https://atcoder.jp/login'
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
        soup = bs(html.text, 'lxml')
        csrf_token = soup.find(attrs={'name': 'csrf_token'}).get('value')
        return csrf_token

    def post(self, url, data=None):
        res = self.session.post(url, data)
        return res

    def get(self, url):
        return self.session.get(url)

    def get_task_screen_name(self, url, prob_type):
        html = self.get(url)
        soup = bs(html.text, 'html5lib')
        task_screen_name = ''
        for tr in soup.find('tbody').find_all('tr'):
            item = tr.find('td').find('a')
            p_type = item.contents[0].lower()
            link = item.get('href')
            if p_type == prob_type:
                # /contests/abc160/tasks/abc160_a という形式で取得できるので、
                # 最後の'abc160_a'の部分を取り出す
                task_screen_name = link.split('/')[-1]
                break
        return task_screen_name

if __name__ == '__main__':
    ac = AtConnector()
    ac.login()
