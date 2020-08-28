#!/usr/bin/env python
from libpycoder.judge import Judge
from argparse import ArgumentParser


def main():
    example = """
    ex1: abc123のd問題をテスト
        python {0} abc 123 d
    ex2: abc123のa問題をテスト（差が1e-6以内かどうか）
        python {0} abc 123 a -e 1e-6e
    ex3: abc123のa問題がテスト通過したら提出（python3）
        python {0} abc 123 a -s p
    ex4: abc123のa問題がテスト通過したら提出（pypy3）
        python {0} abc 123 a -s pp
    ex5: テストの成否を無視して提出
        python {0} abc 123 a -s p -f
    ex6: 特定のテストのみを実行
        python {0} abc 123 a -d 01
    """.format(__file__)

    argparser = ArgumentParser(usage=example)
    argparser.add_argument('contest_id',
                           type=str,
                           help='コンテストID')
    argparser.add_argument('problem_type',
                           type=str,
                           help='テスト対象の問題指定(a ~ f)')
    argparser.add_argument('-v', '--verbose',
                           action='store_true',
                           help='各テストケースの入力、出力を表示')
    argparser.add_argument('-e', '--error',
                           type=float,
                           help='出力誤差の値を判定')
    argparser.add_argument('-s', '--submit',
                           type=str,
                           choices=['p', 'pp'],
                           help='テストに全て通過した場合に提出する')
    argparser.add_argument('-f', '--force',
                           action='store_true',
                           help='テストの成否を無視して強制的に提出する')
    argparser.add_argument('-d', '--debug',
                           type=str,
                           help='テストケースのprefix')

    args = argparser.parse_args()

    if args.contest_id[:3] in ['abc','arc','agc']:
        contest_type = args.contest_id[:3]
        contest_id = args.contest_id[3:]
    else:
        contest_type = 'others'
        contest_id = args.contest_id

    judge = Judge(contest_type,
                  contest_id,
                  args.problem_type)

    if not args.debug:
        result = judge.test_all(verbose=args.verbose, diff=args.error)
    else:
        judge.test_debug(args.debug)
        return None

    if (result or args.force) and args.submit:
        judge.submit(args.submit)


if __name__ == '__main__':
    main()
