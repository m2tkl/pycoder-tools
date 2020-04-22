import requests
from bs4 import BeautifulSoup
import config
from .atconnector import AtConnector
from .pathmanager import PathManager
from .atscraper import extract_sample_test_cases_from_prob_page
import sys, os

class TestMaker():
    def __init__(self, contest_type, contest_id):
        self.contest_type = contest_type
        self.contest_id = contest_id
        self.pm = PathManager(contest_type, contest_id)

    def fetch_sample_cases(self):
        ac = AtConnector()
        ac.init_session()
        prob_urls = ac.get_prob_urls(self.contest_type, self.contest_id)
        problems = ['a', 'b', 'c', 'd', 'e', 'f']
        for p in problems:
            print('*', end='')
            url = prob_urls[p]
            if url == '': continue
            # login済みのセッションを利用して、HTMLを取得する
            res = ac.get(url)
            soup = BeautifulSoup(res.text, 'html5lib')
            sample_test_cases = extract_sample_test_cases_from_prob_page(res.text)
            file_dir = self.pm.get_tests_dir_path(p)
            for idx, sample_case in sample_test_cases.items():
                iname = '0' + str(idx) + '_input.txt'
                oname = '0' + str(idx) + '_output.txt'
                with open(file_dir + iname, 'w') as f: f.write(sample_case.input)
                with open(file_dir + oname, 'w') as f: f.write(sample_case.output)
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
        with open(file_dir + prefix + '_input.txt', 'w') as f: f.write(input_case.rstrip())
        with open(file_dir + prefix + '_output.txt', 'w') as f: f.write(output_case)
        print('Done!')