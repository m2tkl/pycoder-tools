import os
import subprocess
import config
from .login import AtConnector
from .pathmanager import PathManager
from utils.pycolor import pprint
from bs4 import BeautifulSoup
import requests

class Judge:
    def __init__(self, contest_type, contest_id, prob_type):
        self.pm = PathManager(contest_type, contest_id)
        self.test_target = self.pm.get_prob_file_path(prob_type)
        self.tests_dir = self.pm.get_tests_dir_path(prob_type)
        self.prob_type = prob_type

        test_files = sorted(os.listdir(self.tests_dir))
        self.test_cases = []
        for i in range(0, len(test_files), 2):
            # 00_input.txt, 00_output.txtをまとめてtest_caseとする
            test_case = (test_files[i], test_files[i+1])
            self.test_cases.append(test_case)

    def test(self, diff=None, verbose=False) -> bool:
        print('test num: {}'.format(len(self.test_cases)))
        all_result = True
        for test in self.test_cases:
            test_input = test[0]
            test_output = test[1]
            prefix = test_input[:2]
            # prefixの２桁目が0の場合はsampleテストケース,それ以外の場合は追加したテストケースを表す
            if prefix[0] == '0':
                pprint('sample_case' + prefix + ' => ', end='', bold=True)
            else:
                pprint('additional_case' + prefix + ' => ', end='', bold=True)

            actual = self.run_program(self.test_target, self.tests_dir+test_input)
            expected = self.get_expected_val(self.tests_dir+test_output)

            # Judge!
            # --diffオプションを指定した場合は誤差を判定する
            if diff: result = self.judge_diff(actual, expected, diff)
            else:    result = self.judge_equal(actual, expected)
            all_result &= result

            with open(self.tests_dir + test_input) as f: input_val = f.read().rstrip()

            # Show results
            self.print_result(result, input_val, actual, expected, verbose)
        return all_result

    def run_program(self, target: str, target_input:str) -> str:
        # ex: python <atcoder-dir-path>/ABC/134/A.py < <atcoder-dir-path>/ABC/134/tests/A/00_input.txt
        command = ['python', target, '<', target_input]
        std = subprocess.run(' '.join(command), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        res = std.stdout.decode('utf-8').rstrip()
        return res

    def get_expected_val(self, file_name: str) -> str:
        with open(file_name, 'r') as f: expected = f.read().rstrip()
        return expected

    def judge_equal(self, actual:str, expected:str) -> bool:
        return actual == expected

    def judge_diff(self, actual: str, expected: str, diff: float):
       return abs(float(expected) - float(actual)) < diff

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

    def submit(self, submit_lang_id):
        ac = AtConnector()
        ac.login()
        submit_url = self.pm.get_submit_url()
        csrf_token = ac.get_csrf_token(submit_url)

        contest_url = self.pm.get_contest_url()
        task_screen_name = ac.get_task_screen_name(contest_url, self.prob_type)

        with open(self.test_target, 'r') as f:
            submit_code = f.read()
        submit_info = {
            "data.TaskScreenName": task_screen_name,
            "csrf_token": csrf_token,
            "data.LanguageId": submit_lang_id,
            "sourceCode": submit_code
        }
        res = ac.post(submit_url, data=submit_info)
        res.raise_for_status()
        if res.status_code == 200:
            print("Submitted!")
        else:
            print("Error in submitting...")
            exit(1)
