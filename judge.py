import sys, os
import subprocess
import config
from utils.pycolor import PyColor
from argparse import ArgumentParser
from bs4 import BeautifulSoup
import requests

PYTHON_ID = 3023
PYPY_ID = 3510

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

    contest_type = args.contest_type
    contest_id = args.contest_id
    problem_type = args.problem_type

    # config.pyにatcoderディレクトリの指定がない場合はカレントディレクトリを指定
    if not config.ATCODER_DIR_PATH == None:
        atcoder_dir_path = config.ATCODER_DIR_PATH
    else:
        atcoder_dir_path = './'

    pc = PyColor()

    target_contest = atcoder_dir_path + contest_type + '/' + contest_id
    test_target = target_contest + '/' + problem_type + '.py'
    tests_dir   = target_contest + '/tests/' + problem_type + '/'

    test_files = sorted(os.listdir(tests_dir))
    test_cases = []
    for i in range(0, len(test_files), 2):
        # 00_input.txt, 00_output.txtをまとめてtest_caseとする
        test_case = (test_files[i], test_files[i+1])
        test_cases.append(test_case)

    print('test num: {}'.format(len(test_cases)))

    for test in test_cases:
        test_input = test[0]
        test_output = test[1]
        prefix = test_input[:2]
        # prefixの２桁目が0の場合はsampleテストケース,1の場合は追加したテストケースを表す
        if prefix[0] == '0':
            pc.pprint('sample_case' + prefix + ' => ', end='', bold=True)
        else:
            pc.pprint('additional_case' + prefix + ' => ', end='', bold=True)

        # テスト実行
        # ex: python <atcoder-dir-path>/abc/134/a.py < <atcoder-dir-path>/abc/134/tests/A/00_input.txt
        command = ['python', test_target, '<', tests_dir + test_input]
        std = subprocess.run(' '.join(command), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

        # Judge!
        with open(tests_dir + test_output) as f:
            expected = f.read().rstrip()
            actual = std.stdout.decode('utf-8').rstrip()

            # --diffオプションを指定した場合は誤差を判定する
            if args.diff:
                is_correct = (abs(float(expected) - float(actual)) < args.diff)
            else:
                is_correct = (expected == actual)

        if args.verbose:
            with open(tests_dir + test_input) as f:
                input_val = f.read().rstrip()

        if is_correct:
            pc.pprint('OK', color='green')
            if args.verbose:
                print('[input]')
                print('{}'.format(input_val))
                print('[output]')
                print('{}'.format(actual))
        else:
            pc.pprint('NG', color='r')
            if args.verbose:
                print('[input]')
                print('{}'.format(input_val))
            pc.pprint('[expected]', color='g')
            pc.pprint('{}'.format(expected), color='g')
            pc.pprint('[actual]', color='r')
            pc.pprint('{}'.format(actual), color='r')

    # is_correct = True かつ submitオプションがある場合
    if is_correct and args.submit:
        if args.submit == 'p':
            submit_lang_id = PYTHON_ID
        else:
            submit_lang_id = PYPY_ID

        source_path = test_target
        with open(source_path, 'r') as f:
            source_code = f.read()

        LOGIN_URL = "https://atcoder.jp/login"
        # セッション開始
        session = requests.session()
        # csrf_token取得
        r = session.get(LOGIN_URL)
        s = BeautifulSoup(r.text, 'lxml')
        csrf_token = s.find(attrs={'name': 'csrf_token'}).get('value')
        # パラメータセット
        login_info = {
            "csrf_token": csrf_token,
            "username": config.USERNAME,
            "password": config.PASSWORD
        }
        result = session.post(LOGIN_URL, data=login_info)
        result.raise_for_status()
        if result.status_code==200:
            print("Login!")
        else:
            print("Failed...")
            exit(1)

        submit_url = 'https://atcoder.jp/contests/' + contest_type + contest_id + '/submit'
        html = session.get(submit_url)
        html.raise_for_status()
        soup = BeautifulSoup(html.text, 'lxml')
        csrf_token = soup.find(attrs={'name': 'csrf_token'}).get('value')
        submit_info = {
            "data.TaskScreenName": contest_type + contest_id + '_' + problem_type,
            "csrf_token": csrf_token,
            "data.LanguageId": submit_lang_id,
            "sourceCode": source_code
        }
        result = session.post(submit_url, data=submit_info)
        result.raise_for_status()

        if result.status_code == 200:
            print("Submitted!")
        else:
            print("Error in submitting...")
