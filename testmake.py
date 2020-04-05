import requests
from bs4 import BeautifulSoup
import config
from utils.login import AtConnector
import sys, os
from argparse import ArgumentParser

class TestMaker():
    def __init__(self, contest_type, contest_id):
        self.contest_type = contest_type
        self.contest_id = contest_id
        if not config.ATCODER_DIR_PATH == None:
            self.atcoder_dir_path = config.ATCODER_DIR_PATH
        else:
            self.atcoder_dir_path = './'

    def __extract_unused_data(self, soup_obj):
        # 英語ケースを削除
        while soup_obj.find('span', class_='lang-en'):
            soup_obj.find('span', class_='lang-en').extract()
        # 入力形式の欄をテストケースとして取得しないように削除
        while soup_obj.find('div', class_='io-style'):
            soup_obj.find('div', class_='io-style').extract()
        return soup_obj

    def fetch_sample_cases(self):
        ac = AtConnector()
        ac.login()
        problems = ['a', 'b', 'c', 'd', 'e', 'f']
        for p in problems:
            print('*', end='')
            # url = 'https://atcoder.jp/contests/abc146/tasks/abc146_a'
            url = \
                'https://atcoder.jp/contests/' \
                + self.contest_type + self.contest_id \
                + '/tasks/'+ self.contest_type + self.contest_id \
                + '_' + p
            # login済みのセッションを利用して、HTMLを取得する
            res = ac.session.get(url)
            # レスポンスの HTML から BeautifulSoup オブジェクトを作る
            soup = BeautifulSoup(res.text, 'html.parser')

            soup = self.__extract_unused_data(soup)
            test_samples = soup.find_all('pre')
            test_case = {}
            count = 0
            for i in range(0, len(test_samples), 2):
                test_case[count] = (test_samples[i].get_text(),
                                    test_samples[i+1].get_text())
                count += 1

            # サンプルケースをファイルへ書き込む
            file_dir = \
                self.atcoder_dir_path + self.contest_type.upper() \
                + '/' + self.contest_id + '/tests/'+ p.upper() + '/'
            for k, v in test_case.items():
                iname = '0' + str(k) + '_input.txt'
                oname = '0' + str(k) + '_output.txt'
                with open(file_dir + iname, 'w') as f: f.write(v[0])
                with open(file_dir + oname, 'w') as f: f.write(v[1])

        print('\nDone!')

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
        file_dir = \
            self.atcoder_dir_path + \
            self.contest_type.upper() + '/' + self.contest_id + \
            '/tests/' + problem_type.upper() + '/'
        tests = os.listdir(file_dir)
        additional_cases = [t for t in tests if t[0] == '1']
        prefix = str(10 + len(additional_cases)//2)
        with open(file_dir + prefix + '_input.txt', 'w') as f: f.write(input_case.rstrip())
        with open(file_dir + prefix + '_output.txt', 'w') as f: f.write(output_case)
        print('Done!')

if __name__ == '__main__':

    example = """
    ex1: abc134のテストケースを取得
        python {0} abc 134
    ex2: abc134のB問題にテストケースを追加
        python {0} abc 134 -a b
    """.format(__file__)

    argparser = ArgumentParser(usage=example)
    argparser.add_argument('contest_type',
                           type=str,
                           help='コンテストの種類')
    argparser.add_argument('contest_id',
                           type=str,
                           help='コンテスト番号')
    argparser.add_argument('-a', '--add',
                           type=str,
                           help='テストケースの追加')

    args = argparser.parse_args()

    tm = TestMaker(args.contest_type, args.contest_id)
    if not args.add:
        tm.fetch_sample_cases()
    else:
        tm.add_test_case(args.add)
