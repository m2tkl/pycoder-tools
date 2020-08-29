import importlib
import requests
import sys
import webbrowser
from typing import Dict
from . import atscraper
from . import langs
from . import atsession

from pathlib import Path
import pickle
import datetime
import os

sys.path.append(str(Path(__file__).resolve().parent.parent))
config = importlib.import_module('config')

ATCODER_URL = 'https://atcoder.jp'
LOGIN_URL = 'https://atcoder.jp/login'
CONTEST_URL = 'https://atcoder.jp/contests/'


class AtConnector:
    def __init__(self):
        self.AS = atsession.AtSession()

    def get(self, url):
        return self.AS.get(url)

    def post(self, url, data=None):
        return self.AS.post(url, data)

    def get_task_screen_name(self,
                             contest_type: str,
                             contest_id: str,
                             prob_type: str) -> str:
        """
        @param contest_type コンテストの種類(abc, arc, ...)
        @param contest_id コンテスト番号
        @param prob_type 問題の種類(a, b, c, d, ...)
        @return task_screen_name
        """
        html = self._get_contest_tasks_page(contest_type, contest_id)
        task_screen_name = atscraper.extract_task_screen_name(html, prob_type)
        return task_screen_name

    def get_prob_urls(self, contest_type: str, contest_id: str) -> Dict[str, str]:
        """コンテスト問題一覧ページから各問題のurlを取得して返す
        @param contest_type abc, arc, agc, ...
        @param contest_id 123, ...
        @return prob_links 各問題へのurlを持つdict
        """
        html = self._get_contest_tasks_page(contest_type, contest_id)
        prob_links = atscraper.extract_prob_links(html)
        for prob_type, link in prob_links.items():
            prob_links[prob_type] = ATCODER_URL + link
        return prob_links

    def _get_contest_tasks_page(
            self,
            contest_type: str,
            contest_id: str) -> str:
        """問題一覧ページのhtmlを取得する.
        @param contest_type コンテストのタイプ(abc, arc, ...)
        @param contest_id コンテスト番号
        @return html 問題一覧ページのhtml
        """
        tasks_url = self._get_tasks_url(contest_type, contest_id)
        res = self.AS.get(tasks_url)
        html = res.text
        return html

    def _get_tasks_url(self, contest_type: str, contest_id: str) -> str:
        """問題一覧ページのurlを返す.
        @param contest_type コンテストのタイプ(abc, arc, ...)
        @param contest_id コンテスト番号
        @return 問題一覧ページのurl
        """
        if contest_type == 'others':
            return CONTEST_URL + contest_id + '/tasks'
        return CONTEST_URL + contest_type + contest_id + '/tasks'

    def _get_submission_result_url(self, contest_type, contest_id):
        """提出結果ページのurlを返す
        @param contest_type コンテストのタイプ
        @param contest_id コンテストの番号
        @return 提出結果ページのurl
        """
        if contest_type == 'others':
            return CONTEST_URL + contest_id + '/submissions/me'
        return CONTEST_URL + contest_type + contest_id + '/submissions/me'

    def _get_submit_url(self, contest_type: str, contest_id: str) -> str:
        """提出ページのurlを返す.
        @param contest_type コンテストのタイプ(abc, arc, ...)
        @param contest_id コンテスト番号
        @return 提出ページのurl
        """
        if contest_type == 'others':
            return CONTEST_URL + contest_id + '/submit'
        return CONTEST_URL + contest_type + contest_id + '/submit'

    def submit(self, contest_type: str, contest_id: str,
               prob_type: str, src: str, lang_type: str) -> None:
        """ソースコードを提出する.
        @param contest_type コンテストのタイプ(abc, arc, ...)
        @param contest_id コンテスト番号
        @param prob_type 問題のタイプ(a, b, c, d, ...)
        @param src 提出コード
        @param lang_type 提出言語
        """
        submit_url = self._get_submit_url(contest_type, contest_id)
        csrf_token = self.get_csrf_token(submit_url)
        task_screen_name = self.get_task_screen_name(contest_type,
                                                     contest_id,
                                                     prob_type)
        lang_ids = langs.get_lang_ids(lang_type)
        # language updateにより言語Idがコンテストによって異なる
        # 場合があるため、それぞれのIdで提出を試みる
        for lang_id in lang_ids:
            submit_info = {"data.TaskScreenName": task_screen_name,
                           "csrf_token": csrf_token,
                           "data.LanguageId": lang_id,
                           "sourceCode": src}
            try:
                res = self.AS.post(submit_url, data=submit_info)
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

    def open_submission_page(self, contest_type, contest_id):
        """引数で指定したコンテストの提出結果ページを開く
        @param contest_type コンテストのタイプ
        @param contest_id コンテスト番号
        """
        result_page_url = self._get_submission_result_url(
            contest_type, contest_id)
        webbrowser.open(result_page_url)
