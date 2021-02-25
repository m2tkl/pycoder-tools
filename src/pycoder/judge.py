#!/usr/bin/env python
from libpycoder.judge import Judge
from argparse import ArgumentParser
from .argutil import split_contest_id


def judge(contest_id, prob_type,
          verbose=False, error=None, debug=None,
          submit=None, force=False):
    """テストケースの判定を行う
    :param contest_id: コンテストの名前(ex: abc001, hogecon2020)
    :param prob_type: 判定対象の問題(a, b, c, ...)
    :param verbose: 判定結果だけでなく入出力も表示する
    :param error: 誤差判定が必要なときに値を指定する
    :param submit: 提出オプション。すべてのテストケースに通過した場合提出する
    :param force: 提出オプション。テストケースに通過しなくても強制的に提出する
    :param debug: デバッグオプション。指定したテストケースのみを表示しつつ実行
    """
    contest = split_contest_id(contest_id)

    judge = Judge(contest.type, contest.name, prob_type)

    if not debug:
        result = judge.test_all(verbose=verbose, diff=error)
    else:
        judge.test_debug(debug)
        return None

    if (result or force) and submit:
        judge.submit(submit)


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

    judge(args.contest_id, args.problem_type,
          args.verbose, args.error, args.debug,
          args.submit, args.force)


if __name__ == '__main__':
    main()
