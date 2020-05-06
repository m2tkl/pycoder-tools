import os
import subprocess
from .atconnector import AtConnector
from .pathmanager import PathManager
from utils.pycolor import pprint
from collections import namedtuple
from typing import Optional
from enum import Enum, auto

def read_file(file_path: str) -> str:
    with open(file_path, 'r') as f:
        content = f.read().rstrip()
    return content


class Result(Enum):
    OK = auto()
    NG = auto()
    TLE = auto()
    RE = auto()


class Judge:
    def __init__(self, contest_type, contest_id, prob_type):
        self.contest_type = contest_type
        self.contest_id = contest_id
        self.prob_type = prob_type
        pm = PathManager(contest_type, contest_id)
        self.target_src_path = pm.get_prob_file_path(prob_type)
        tests_dir = pm.get_tests_dir_path(prob_type)
        self.test_case_files = self.get_test_case_paths(tests_dir)

    def get_test_files(self, test_dir_path):
        test_files = list(map(
            lambda x: test_dir_path + x,
            sorted(os.listdir(test_dir_path))))
        return test_files

    def get_test_case_paths(self, test_dir_path):
        test_files = self.get_test_files(test_dir_path)
        in_files = test_files[0::2]
        out_files = test_files[1::2]
        TestCase = namedtuple('TestCase', ['input', 'output'])
        test_case_files = [TestCase(*test_case) for test_case in zip(in_files, out_files)]
        return test_case_files

    def test_all(self, diff: float = None, verbose: bool = False) -> bool:
        """全てのテストスイートを実行し, 結果を返す.
        @param diff テスト時に誤差を判定に使う場合に指定する.
        @param verbose 結果表示を冗長にする場合Trueを指定する.
        @return total_result 全てのテストケースに通過すればTrue, そうでなければFalse
        """
        print('test num: {}'.format(len(self.test_case_files)))
        total_result = True
        for test_case_file in self.test_case_files:
            result = self.test(
                self.target_src_path,
                test_case_file.input,
                test_case_file.output,
                diff, verbose)
            total_result &= result
        return total_result

    def test_debug(self, test_case_prefix: str):
        test_case_file = None
        for tc in self.test_case_files:
            if tc.input.split('/')[-1][:2] == test_case_prefix:
                test_case_file = tc
                break
        result = self.test(
            self.target_src_path,
            test_case_file.input,
            test_case_file.output,
            None, True,
        )

    def test(
            self,
            run_target_path,
            test_input_path,
            test_output_path,
            diff: float = None,
            verbose: bool = False) -> bool:
        """テストケースを実行し,結果を返す.
        @param run_target_path テスト対象プログラムのpath
        @param test_input_path テストの入力
        @param test_output_path 期待される出力
        @param diff 誤差判定オプション
        @param verbose 詳細結果表示オプション
        @return result 判定結果
        """
        res, actual = self.run_test(
            run_target_path,
            test_input_path,
            test_output_path,
            diff)
        self.print_result(
            res,
            test_input_path,
            test_output_path,
            actual,
            verbose)
        return res == Result.OK

    def run_test(
                self,
                target: str,
                input_path: str,
                output_path: str,
                diff: float) -> Optional[str]:
        """targetプログラムに入力を与え,実行結果(出力)を返す.
        @param target 実行対象プログラムのpath
        @param target_input 入力ファイルのpath
        @return res 実行結果(出力)
        """
        command = ' '.join(['python', target, '<', input_path])
        try:
            std = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=2.5,
                shell=True,
                check=True)
        except subprocess.TimeoutExpired:
            res = Result.TLE
            actual_output = None
        except subprocess.CalledProcessError as e:
            res = Result.RE
            actual_output = e.output.decode('utf-8').rstrip()
        else:
            actual_output = std.stdout.decode('utf-8').rstrip()
            expected_output = read_file(output_path)
            res = self.judge(actual_output, expected_output, diff)
        return (res, actual_output)

    def judge(self, actual: str, expected: str, diff: float = None):
        """正誤判定を行う.
        @param actual 実際の出力
        @param expected 期待される出力
        @param diff 指定された場合は誤差を正誤判定に用いる.
        @return 正解ならばTrue, 不正解ならばFalse
        """
        if diff:
            if abs(float(expected) - float(actual)) < diff:
                return Result.OK
        if actual == expected:
            return Result.OK
        return Result.NG

    def print_result(
            self,
            result: bool,
            input_file,
            output_file,
            actual,
            verbose: bool = None):
        """テスト実行結果の表示を行う.
        @param result 正誤判定
        @param input_file テストの入力
        @param actual 実行結果
        @param expected 期待される出力
        @param verbose Trueの場合,正誤判定だけでなく,入出力の値も表示する
        """
        prefix = input_file.split('/')[-1][:2]
        pprint(prefix + '_test_case' + ' => ', end='', bold=True)

        # 結果(OK or NG)の表示
        result_color = 'green' if result == Result.OK else 'red'
        pprint('{}'.format(result.name), color=result_color)

        if verbose:
            input_val = read_file(input_file)
            expected = read_file(output_file)
            pprint('[input]', color='cyan')
            print(input_val)
            if result == Result.OK:
                pprint('[output]', color='cyan')
                print(actual)
                print()
            if result == Result.NG:
                pprint('[expected]', color='green')
                pprint(expected, color='green', bold=False)
                pprint('[actual]', color='red')
                pprint(actual, color='red', bold=False)
                print()
            if result == Result.RE:
                pprint(actual, color='red', bold=False)
                print()
            if result == Result.TLE:
                pprint('[input]', color='red')
                pprint(input_val, color='red', bold=False)
                print()

    def submit(self, lang_type):
        ac = AtConnector()
        ac.init_session()
        submit_code = read_file(self.target_src_path)
        ac.submit(self.contest_type,
                  self.contest_id,
                  self.prob_type,
                  submit_code,
                  lang_type)
