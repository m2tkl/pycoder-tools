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
        self.test_case_files = [TestCase(*test_case) for test_case in zip(input_files, output_files)]

    def test(self, diff: float=None, verbose: bool=False) -> bool:
        """テストスイートを実行する.
        @param diff テスト時に誤差を判定に使う場合に指定する.
        @param verbose 結果表示を冗長にする場合Trueを指定する.
        """
        print('test num: {}'.format(len(self.test_case_files)))

        total_result = True
        for test_case_file in self.test_case_files:
            run_target_path = self.test_target
            test_input_path = self.tests_dir + test_case_file.input
            test_output_path = self.tests_dir + test_case_file.output

            actual = self.run_program(run_target_path, test_input_path)
            expected = self.read_file(test_output_path)
            result = self.judge(actual, expected, diff)
            total_result &= result

            self.print_result(result, test_case_file.input, actual, expected, verbose)

        return total_result

    def run_program(self, target: str, target_input:str) -> str:
        # ex: python <atcoder-dir-path>/ABC/134/A.py < <atcoder-dir-path>/ABC/134/tests/A/00_input.txt
        command = ' '.join(['python', target, '<', target_input])
        std = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        res = std.stdout.decode('utf-8').rstrip()
        return res

    def read_file(self, file_name: str) -> str:
        with open(file_name, 'r') as f:
            content = f.read().rstrip()
        return content

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

    def print_result(self, result: bool, input_file, actual, expected, verbose: bool = None):
        """テスト実行結果の表示を行う.
        @param result 正誤判定
        @param input_file テストの入力
        @param actual 実行結果
        @param expected 期待される出力
        @param verbose Trueの場合,正誤判定だけでなく,入出力の値も表示する
        """
        # どのテストケースであるかを表示する.
        prefix = input_file[:2]
        if prefix[0] == '0': pprint('sample_case' + prefix + ' => ', end='', bold=True)
        else: pprint('additional_case' + prefix + ' => ', end='', bold=True)

        # 結果(OK or NG)の表示
        if result == True: pprint('OK', color='g')
        else: pprint('NG', color='r')

        # verboseオプションありの場合は, 入出力を表示する.
        if verbose:
            with open(self.tests_dir + input_file) as f:
                input_val = f.read().rstrip()
            print('[input]\n{}'.format(input_val))
            if result == True:
                print('[output]\n{}'.format(actual))

        # 不正解の場合はverboseオプションに関わらず出力を表示する.
        if result == False:
            pprint('[expected]\n{}'.format(expected), color='g')
            pprint('[actual]\n{}'.format(actual), color='r')

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
