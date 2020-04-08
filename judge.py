from libpycoder.judge import Judge
from argparse import ArgumentParser

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

    judge = Judge(args.contest_type,
                  args.contest_id,
                  args.problem_type)

    result = judge.test(verbose=args.verbose, diff=args.diff)

    if result and args.submit:
        if args.submit == 'p':
            submit_lang_id = PYTHON_ID
        elif args.submit == 'pp':
            submit_lang_id = PYPY_ID
        else:
            print('This option not supported.')
            exit(1)
        judge.submit(submit_lang_id)
