#!/usr/bin/env python
from libpycoder.testmake import TestMaker
from argparse import ArgumentParser
from .argutil import split_contest_id


def add_test_case(contest_id, task):
    """テストケースを追加する
    :param contest_id: コンテストの名前(ex: abc001, hogecon2020)
    :param task: 追加対象の問題(a, b, c, ...)
    """
    contest = split_contest_id(contest_id)
    tm = TestMaker(contest.type, contest.name)
    tm.add_test_case(task)


def set_contest(contest_id):
    """コンテストを準備する
    :param contest_id: コンテストの名前(ex: abc001, hogecon2020)
    :param add: テストケースの追加時に指定
    """
    contest = split_contest_id(contest_id)
    tm = TestMaker(contest.type, contest.name)
    tm.fetch_sample_cases()


def main():
    example = """
    ex1: abc134の準備
        python {0} abc134
    ex2: abc134のB問題にテストケースを追加
        python {0} abc134 -a b
    """.format(__file__)

    argparser = ArgumentParser(usage=example)
    argparser.add_argument('contest_id',
                           type=str,
                           help='コンテストID')
    argparser.add_argument('-a', '--add',
                           type=str,
                           help='テストケースの追加')

    args = argparser.parse_args()

    if not args.add:
        set_contest(args.contest_id)
    else:
        add_test_case(args.contest_id, args.add)


if __name__ == '__main__':
    main()
