import sys, os
import subprocess
import config
from utils.pycolor import PyColor
from argparse import ArgumentParser

if __name__ == '__main__':
    example = """
    ex1: abc134のd問題をテスト
        python {0} abc 134 d
    ex2: abc142のa問題をテスト（差が1e-6以内かどうか）
        python {0} abc 142 a -d 1e-6
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
