import os
import subprocess
import config
from .atconnector import AtConnector
from .pathmanager import PathManager
from utils.pycolor import pprint
from bs4 import BeautifulSoup
import requests
from collections import namedtuple

class Judge:
    def __init__(self, contest_type, contest_id, prob_type):
        self.pm = PathManager(contest_type, contest_id)
        self.test_target = self.pm.get_prob_file_path(prob_type)
        self.tests_dir = self.pm.get_tests_dir_path(prob_type)
        self.contest_type = contest_type
        self.contest_id = contest_id
        self.prob_type = prob_type

        test_files = sorted(os.listdir(self.tests_dir))
        input_files = test_files[0::2]
        output_files = test_files[1::2]
        TestCase = namedtuple('TestCase', ['input', 'output'])
        self.test_cases = [TestCase(*test_case) for test_case in zip(input_files, output_files)]

    def test(self, diff=None, verbose=False) -> bool:
        print('test num: {}'.format(len(self.test_cases)))
        total_result = True
        for test_case in self.test_cases:
            prefix = test_case.input[:2]
            # prefixの2桁目が0の場合はsampleテストケース,それ以外は追加したテストケースを表す
            if prefix[0] == '0':
                pprint('sample_case' + prefix + ' => ', end='', bold=True)
            else:
                pprint('additional_case' + prefix + ' => ', end='', bold=True)

            actual = self.run_program(self.test_target, self.tests_dir + test_case.input)
            expected = self.get_expected_val(self.tests_dir + test_case.output)

            result = self.judge(actual, expected, diff)

            total_result &= result

            with open(self.tests_dir + test_case.input) as f:
                input_val = f.read().rstrip()

            # Show results
            self.print_result(result, input_val, actual, expected, verbose)
        return total_result

    def run_program(self, target: str, target_input:str) -> str:
        # ex: python <atcoder-dir-path>/ABC/134/A.py < <atcoder-dir-path>/ABC/134/tests/A/00_input.txt
        command = ['python', target, '<', target_input]
        std = subprocess.run(' '.join(command), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        res = std.stdout.decode('utf-8').rstrip()
        return res

    def get_expected_val(self, file_name: str) -> str:
        with open(file_name, 'r') as f: expected = f.read().rstrip()
        return expected

    def judge(self, actual: str, expected: str, diff: float = None):
        """正誤判定を行う.
        @param actual 実際の出力
        @param expected 期待される出力
        @param diff 指定された場合は誤差を正誤判定に用いる.
        @return 正解ならばTrue, 不正解ならばFalse
        """
        if diff != None:
            return abs(float(expected) - float(actual)) < diff
        else:
            return actual == expected

    def print_result(self, result: bool, input_val, actual, expected, verbose: bool = None):
        if result:
            pprint('OK', color='green')
            if verbose:
                print('[input]')
                print('{}'.format(input_val))
                print('[output]')
                print('{}'.format(actual))
        else:
            pprint('NG', color='r')
            if verbose:
                print('[input]')
                print('{}'.format(input_val))
            pprint('[expected]', color='g')
            pprint('{}'.format(expected), color='g')
            pprint('[actual]', color='r')
            pprint('{}'.format(actual), color='r')

    def submit(self, lang_type):
        ac = AtConnector()
        ac.init_session()
        with open(self.test_target, 'r') as f:
            submit_code = f.read()
        ac.submit(self.contest_type,
                  self.contest_id,
                  self.prob_type,
                  submit_code,
                  lang_type)
