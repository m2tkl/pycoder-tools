import sys, os
import subprocess
import config
from utils.pycolor import PyColor
from libpycoder.login import AtConnector
from libpycoder.pathmanager import PathManager
from argparse import ArgumentParser
from bs4 import BeautifulSoup
import requests

PYTHON_ID = 3023
PYPY_ID = 3510

class Judge:
    def __init__(self, contest_type, contest_id, prob_type):
        self.pm = PathManager(contest_type, contest_id)
        self.test_target = self.pm.get_prob_file_path(prob_type)
        self.tests_dir = self.pm.get_tests_dir_path(prob_type)

        self.task_screen_name = contest_type + contest_id + '_' + prob_type

        test_files = sorted(os.listdir(self.tests_dir))
        self.test_cases = []
        for i in range(0, len(test_files), 2):
            # 00_input.txt, 00_output.txtをまとめてtest_caseとする
            test_case = (test_files[i], test_files[i+1])
            self.test_cases.append(test_case)

    def test(self, diff=None, verbose=False):
        pc = PyColor()
        print('test num: {}'.format(len(self.test_cases)))
        for test in self.test_cases:
            test_input = test[0]
            test_output = test[1]
            prefix = test_input[:2]
            # prefixの２桁目が0の場合はsampleテストケース,1の場合は追加したテストケースを表す
            if prefix[0] == '0':
                pc.pprint('sample_case' + prefix + ' => ', end='', bold=True)
            else:
                pc.pprint('additional_case' + prefix + ' => ', end='', bold=True)
            # テスト実行
            # ex: python <atcoder-dir-path>/ABC/134/A.py < <atcoder-dir-path>/abc/134/tests/A/00_input.txt
            command = ['python', self.test_target, '<', self.tests_dir + test_input]
            std = subprocess.run(' '.join(command), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

            # Judge!
            with open(self.tests_dir + test_output) as f:
                expected = f.read().rstrip()
                actual = std.stdout.decode('utf-8').rstrip()
                # --diffオプションを指定した場合は誤差を判定する
                if diff:
                    is_correct = (abs(float(expected) - float(actual)) < args.diff)
                else:
                    is_correct = (expected == actual)
            if verbose:
                with open(self.tests_dir + test_input) as f:
                    input_val = f.read().rstrip()
            if is_correct:
                pc.pprint('OK', color='green')
                if verbose:
                    print('[input]')
                    print('{}'.format(input_val))
                    print('[output]')
                    print('{}'.format(actual))
            else:
                pc.pprint('NG', color='r')
                if verbose:
                    print('[input]')
                    print('{}'.format(input_val))
                pc.pprint('[expected]', color='g')
                pc.pprint('{}'.format(expected), color='g')
                pc.pprint('[actual]', color='r')
                pc.pprint('{}'.format(actual), color='r')
        return is_correct

    def submit(self, submit_lang_id):
        ac = AtConnector()
        ac.login()
        with open(self.test_target, 'r') as f:
            submit_code = f.read()
        submit_url = self.pm.get_submit_url()
        html = ac.session.get(submit_url)
        html.raise_for_status()
        soup = BeautifulSoup(html.text, 'lxml')
        csrf_token = soup.find(attrs={'name': 'csrf_token'}).get('value')
        submit_info = {
            "data.TaskScreenName": self.task_screen_name,
            "csrf_token": csrf_token,
            "data.LanguageId": submit_lang_id,
            "sourceCode": submit_code
        }
        result = ac.session.post(submit_url, data=submit_info)
        result.raise_for_status()
        if result.status_code == 200:
            print("Submitted!")
        else:
            print("Error in submitting...")
            exit(1)

if __name__ == '__main__':
    example = """
    ex1: abc134のd問題をテスト
        python {0} abc 134 d
    ex2: abc142のa問題をテスト（差が1e-6以内かどうか）
        python {0} abc 142 a -d 1e-6e
    ex3: abc142のa問題がテスト通過したら提出（python3）
        python {0} abc 142 a -s p
    ex4: abc142のa問題がテスト通過したら提出（pypy3）
        python {0} abc 142 a -s pp
    """.format(__file__)

    argparser = ArgumentParser(usage=example)
    argparser.add_argument('contest_type',
                           type=str,
                           help='コンテストの種類')
    argparser.add_argument('contest_id',
                           type=str,
                           help='コンテスト番号')
    argparser.add_argument('problem_type',
                           type=str,
                           help='テスト対象の問題指定(a ~ f)')
    argparser.add_argument('-v', '--verbose',
                           action='store_true',
                           help='各テストケースの入力、出力を表示')
    argparser.add_argument('-d', '--diff',
                           type=float,
                           help='出力誤差の値を判定')
    argparser.add_argument('-s', '--submit',
                           type=str,
                           choices=['p', 'pp'],
                           help='テストに全て通過した場合に提出する')

    args = argparser.parse_args()

    judge = Judge(args.contest_type,
                  args.contest_id,
                  args.problem_type)

    result = judge.test(verbose=args.verbose, diff=args.diff)

    if result and args.submit:
        if args.submit == 'p':
            submit_lang_id = PYTHON_ID
        elif args.submit == 'pp':
            submit_lang_id = PYPY_ID
        else:
            print('This option not supported.')
            exit(1)
        judge.submit(submit_lang_id)
