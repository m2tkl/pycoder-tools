from .atconnector import AtConnector
from .pathmanager import PathManager
from .atscraper import extract_sample_test_cases_from_prob_page
import sys
import shutil
import os
from pathlib import Path
import importlib

sys.path.append(str(Path(__file__).resolve().parent.parent))
config = importlib.import_module('config')


class TestMaker():
    def __init__(self, contest_type, contest_id):
        self.contest_type = contest_type
        self.contest_id = contest_id
        self.pm = PathManager(contest_type, contest_id)

    def fetch_sample_cases(self):
        """サンプルテストケースを取得し,指定ディレクトリに書き込む.
        """
        ac = AtConnector()
        prob_urls = ac.get_prob_urls(self.contest_type, self.contest_id)
        self.make_directory(prob_urls.keys())
        for p, url in prob_urls.items():
            url = prob_urls[p]
            if url == '':
                continue
            # login済みのセッションを利用して、HTMLを取得する
            res = ac.get(url)
            sample_test_cases = extract_sample_test_cases_from_prob_page(
                res.text)
            file_dir = self.pm.get_tests_dir_path(p)
            print('{} => '.format(p), end='')
            is_exist_sample_calse = True
            for idx, sample_case in sample_test_cases.items():
                if sample_case is None:
                    is_exist_sample_calse = False
                    break
                iname = '0' + str(idx) + '_input.txt'
                oname = '0' + str(idx) + '_output.txt'
                with open(file_dir + iname, 'w') as f:
                    f.write(sample_case.input)
                with open(file_dir + oname, 'w') as f:
                    f.write(sample_case.output)
            if is_exist_sample_calse:
                print('o')
            else:
                print('x')
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
        file_dir = self.pm.get_tests_dir_path(problem_type)
        tests = os.listdir(file_dir)
        additional_cases = [t for t in tests if t[0] == '1']
        prefix = str(10 + len(additional_cases)//2)
        with open(file_dir + prefix + '_input.txt', 'w') as f:
            f.write(input_case.rstrip())
        with open(file_dir + prefix + '_output.txt', 'w') as f:
            f.write(output_case)
        print('Done!')

    def make_directory(self, prob_types):
        dir_name = self.pm.ATCODER_DIR
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        for pt in prob_types:
            file_name = dir_name + pt + '.py'
            if not os.path.exists(file_name):
                template = config.TEMPLATE_FILE or './template/template.py'
                shutil.copy(template, file_name)
        test_dir_name = dir_name + 'tests/'
        if not os.path.exists(test_dir_name):
            for pt in prob_types:
                os.makedirs(test_dir_name + pt)
