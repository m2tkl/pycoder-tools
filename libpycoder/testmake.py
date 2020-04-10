import requests
from bs4 import BeautifulSoup
import config
from .login import AtConnector
from .pathmanager import PathManager
import sys, os

class TestMaker():
    def __init__(self, contest_type, contest_id):
        self.contest_type = contest_type
        self.contest_id = contest_id
        self.pm = PathManager(contest_type, contest_id)
        self.ac = AtConnector()
        self.ac.login()

    def __extract_unused_data(self, soup_obj):
        # 英語ケースを削除
        while soup_obj.find('span', class_='lang-en'):
            soup_obj.find('span', class_='lang-en').extract()
        # 入力形式の欄をテストケースとして取得しないように削除
        while soup_obj.find('div', class_='io-style'):
            soup_obj.find('div', class_='io-style').extract()
        return soup_obj

    def fetch_sample_cases(self):
        problems = ['a', 'b', 'c', 'd', 'e', 'f']
        prob_urls = self.get_prob_urls_from_contest_page()
        for p in problems:
            print('*', end='')
            url = prob_urls[p]
            if url == '': continue
            # login済みのセッションを利用して、HTMLを取得する
            res = self.ac.session.get(url)
            # レスポンスの HTML から BeautifulSoup オブジェクトを作る
            soup = BeautifulSoup(res.text, 'html5lib')
            soup = self.__extract_unused_data(soup)
            test_samples = soup.find_all('pre')
            test_case = {}
            count = 0
            for i in range(0, len(test_samples), 2):
                test_case[count] = (test_samples[i].get_text(),
                                    test_samples[i+1].get_text())
                count += 1
            # サンプルケースをファイルへ書き込む
            file_dir = self.pm.get_tests_dir_path(p)
            for k, v in test_case.items():
                iname = '0' + str(k) + '_input.txt'
                oname = '0' + str(k) + '_output.txt'
                with open(file_dir + iname, 'w') as f: f.write(v[0])
                with open(file_dir + oname, 'w') as f: f.write(v[1])
        print('\nDone!')

    def get_prob_urls_from_contest_page(self):
        """コンテスト問題一覧ページから各問題のurlを取得して返す
        Args:
        Returns:
            urls: 各問題のurl
        """
        contest_url = self.pm.get_contest_url()
        res = self.ac.session.get(contest_url)
        soup = BeautifulSoup(res.text, 'html5lib')

        urls = {'a': '', 'b': '', 'c': '', 'd': '', 'e': '', 'f': ''}
        for tbody in soup.find_all('tbody'):
            for tr in tbody.find_all('tr'):
                item = tr.find('td').find('a')
                prob_type = item.contents[0].lower()
                url = item.get('href')
                urls[prob_type] = 'https://atcoder.jp' + url
        return urls

    def add_test_case(self, problem_type):
        print('Input:')
        input_case = ''
        s = sys.stdin.readline()
        while not s == '\n':
            input_case += s
            s = sys.stdin.readline()
        print('Output:')
        output_case = ''
        s = sys.stdin.readline()
        while not s == '\n':
            output_case += s
            s = sys.stdin.readline()
        file_dir = self.pm.get_tests_dir_path(problem_type)
        tests = os.listdir(file_dir)
        additional_cases = [t for t in tests if t[0] == '1']
        prefix = str(10 + len(additional_cases)//2)
        with open(file_dir + prefix + '_input.txt', 'w') as f: f.write(input_case.rstrip())
        with open(file_dir + prefix + '_output.txt', 'w') as f: f.write(output_case)
        print('Done!')