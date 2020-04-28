import sys
import os
from pathlib import Path
import importlib
from unittest.mock import patch
from unittest.mock import MagicMock
import pytest
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from libpycoder.judge import Judge
from libpycoder import judge

class TestJudge:
    def test_init(self, setup):
        judge_obj = Judge('abc', '123', 'a')
        # 判定対象のファイルパスをチェック
        expected = '/Users/hoge/atcoder/ABC/123/A.py'
        actual = judge_obj.target_src_path
        assert actual == expected

        # テストスイートのパスをチェック
        expected = [('/Users/hoge/atcoder/ABC/123/tests/A/00_input.txt',
                    '/Users/hoge/atcoder/ABC/123/tests/A/00_output.txt'),
                    ('/Users/hoge/atcoder/ABC/123/tests/A/01_input.txt',
                    '/Users/hoge/atcoder/ABC/123/tests/A/01_output.txt')]
        actual = judge_obj.test_case_files
        assert actual[0][0] == expected[0][0]
        assert actual[0][1] == expected[0][1]
        assert actual[1][0] == expected[1][0]
        assert actual[1][1] == expected[1][1]

    @patch.object(Judge, 'get_test_files')
    def test_test(
            self,
            mock_method,
            setup_run_target, setup_test_files):
        mock_method.return_value = setup_test_files
        run_target_path = setup_run_target
        test_input_path = setup_test_files[0]
        test_output_path = setup_test_files[1]
        judge_obj = Judge('abc', '123', 'a')
        # 期待通りの出力結果であればTrue
        assert judge_obj.test(run_target_path, test_input_path, test_output_path) == True

        # 誤った出力結果となった場合、False
        another_test_output_path = setup_test_files[3]
        assert judge_obj.test(run_target_path, test_input_path, another_test_output_path) == False

    @patch.object(Judge, 'test')
    @patch.object(Judge, 'get_test_files')
    def test_test_all_all_OK(
                self,
                mock_get_test_files, mock_test,
                setup_test_files):
        """
        全てのテストケースに通過した場合はTrue.
        """
        mock_test.return_value = True
        mock_get_test_files.return_value = setup_test_files
        judge_obj = Judge('abc', '123', 'a')
        total_result = judge_obj.test_all()
        assert total_result == True
        # テストケースは2つあり,judge.test()は2回呼ばれる
        assert mock_test.call_count == 2

    @patch.object(Judge, 'test')
    @patch.object(Judge, 'get_test_files')
    def test_test_all_not_all_OK(
                self,
                mock_get_test_files, mock_test,
                setup_test_files):
        """
        1つのテスト結果がFalseの場合,全体の結果はFalseになる.
        """
        mock_test.side_effect = [True, False]
        mock_get_test_files.return_value = setup_test_files
        judge_obj = Judge('abc', '123', 'a')
        total_result = judge_obj.test_all()
        assert total_result == False
        # テストケースは2つあり,judge.test()は2回呼ばれる
        assert mock_test.call_count == 2

    @pytest.mark.skip(reason='pytestskip')
    def test_run_program(self):
        pass

    def test_judge_normal(self, setup):
        judge_obj = Judge('abc', '123', 'a')
        expected_output = '1 2 3'
        actual_output = '1 2 3'
        assert judge_obj.judge(expected_output, actual_output) == True

        wrong_output = '11 22 33'
        assert judge_obj.judge(expected_output, wrong_output) == False

    def test_judge_diff(self, setup):
        judge_obj = Judge('abc', '123', 'a')
        expected_output = 0.000011
        actual_output = 0.00001
        assert judge_obj.judge(expected_output, actual_output, diff=1e-6) == True
        assert judge_obj.judge(expected_output, actual_output, diff=1e-7) == False

    @pytest.mark.skip(reason='pytestskip')
    def test_print_result(self):
        pass

    @pytest.mark.skip(reason='pytestskip')
    def test_submit(self):
        pass
