import os
import subprocess
from .atconnector import AtConnector
from .pathmanager import PathManager
from utils.pycolor import pprint
from collections import namedtuple


def read_file(file_path: str) -> str:
    with open(file_path, 'r') as f:
        content = f.read().rstrip()
    return content


class Judge:
    def __init__(self, contest_type, contest_id, prob_type):
        self.contest_type = contest_type
        self.contest_id = contest_id
        self.prob_type = prob_type

        pm = PathManager(contest_type, contest_id)
        self.target_src_path = pm.get_prob_file_path(prob_type)
        tests_dir = pm.get_tests_dir_path(prob_type)
        test_files = list(map(
            lambda x: tests_dir + x,
            sorted(os.listdir(tests_dir))))
        in_files = test_files[0::2]
        out_files = test_files[1::2]
        TestCase = namedtuple('TestCase', ['input', 'output'])
        self.test_case_files = [TestCase(*test_case)
                                for test_case in zip(in_files, out_files)]

    def test_all(self, diff: float = None, verbose: bool = False) -> bool:
        """全てのテストスイートを実行し, 結果を返す.
        @param diff テスト時に誤差を判定に使う場合に指定する.
        @param verbose 結果表示を冗長にする場合Trueを指定する.
        """
        print('test num: {}'.format(len(self.test_case_files)))
        total_result = True
        for test_case_file in self.test_case_files:
            run_target_path = self.target_src_path
            test_input_path = test_case_file.input
            test_output_path = test_case_file.output
            result = self.test(
                run_target_path,
                test_input_path,
                test_output_path,
                diff, verbose)
            total_result &= result
        return total_result

    def test(
            self, run_target_path,
            test_input_path, test_output_path,
            diff: float = None, verbose: bool = False) -> bool:
        """テストケースを実行し,結果を返す.
        @param run_target_path テスト対象プログラムのpath
        @param test_input_path テストの入力
        @param test_output_path 期待される出力
        @param diff 誤差判定オプション
        @param verbose 詳細結果表示オプション
        @return result 判定結果
        """
        actual = self.run_program(run_target_path, test_input_path)
        expected = read_file(test_output_path)
        result = self.judge(actual, expected, diff)
        self.print_result(result, test_input_path, actual, expected, verbose)
        return result

    def run_program(self, target: str, target_input: str) -> str:
        """targetプログラムに入力を与え,実行結果(出力)を返す.
        @param target 実行対象プログラムのpath
        @param target_input 入力ファイルのpath
        @return res 実行結果(出力)
        """
        # ex: python /hoge/ABC/134/A.py < /hoge/ABC/134/tests/A/00_input.txt
        command = ' '.join(['python', target, '<', target_input])
        std = subprocess.run(command, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, shell=True)
        res = std.stdout.decode('utf-8').rstrip()
        return res

    def judge(self, actual: str, expected: str, diff: float = None):
        """正誤判定を行う.
        @param actual 実際の出力
        @param expected 期待される出力
        @param diff 指定された場合は誤差を正誤判定に用いる.
        @return 正解ならばTrue, 不正解ならばFalse
        """
        if diff is not None:
            return abs(float(expected) - float(actual)) < diff
        else:
            return actual == expected

    def print_result(
            self,
            result: bool,
            input_file,
            actual, expected,
            verbose: bool = None):
        """テスト実行結果の表示を行う.
        @param result 正誤判定
        @param input_file テストの入力
        @param actual 実行結果
        @param expected 期待される出力
        @param verbose Trueの場合,正誤判定だけでなく,入出力の値も表示する
        """
        # どのテストケースであるかを表示する.
        prefix = input_file.split('/')[-1][:2]
        if prefix[0] == '0':
            pprint('sample_case' + prefix + ' => ', end='', bold=True)
        else:
            pprint('additional_case' + prefix + ' => ', end='', bold=True)

        # 結果(OK or NG)の表示
        if result:
            pprint('OK', color='green')
        else:
            pprint('NG', color='red')

        # verboseオプションありの場合は, 入出力を表示する.
        if verbose:
            input_val = read_file(input_file)
            print('[input]\n{}'.format(input_val))
            if result:
                print('[output]\n{}'.format(actual))

        # 不正解の場合はverboseオプションに関わらず出力を表示する.
        if not result:
            pprint('[expected]\n{}'.format(expected), color='green')
            pprint('[actual]\n{}'.format(actual), color='red')

    def submit(self, lang_type):
        ac = AtConnector()
        ac.init_session()
        submit_code = read_file(self.target_src_path)
        ac.submit(self.contest_type,
                  self.contest_id,
                  self.prob_type,
                  submit_code,
                  lang_type)
