from libpycoder.testmake import TestMaker
from argparse import ArgumentParser


def main():
    example = """
    ex1: abc134の準備
        python {0} abc 134
    ex2: abc134のB問題にテストケースを追加
        python {0} abc 134 -a b
    """.format(__file__)

    argparser = ArgumentParser(usage=example)
    # argparser.add_argument('contest_type',
    #                        type=str,
    #                        help='コンテストの種類')
    argparser.add_argument('contest_id',
                           type=str,
                           help='コンテストID')
    argparser.add_argument('-a', '--add',
                           type=str,
                           help='テストケースの追加')

    args = argparser.parse_args()

    if args.contest_id[:3] in ['abc','arc','agc']:
        contest_type = args.contest_id[:3]
        contest_id = args.contest_id[3:]
    else:
        contest_type = 'others'
        contest_id = args.contest_id

    tm = TestMaker(contest_type, contest_id)
    if not args.add:
        tm.fetch_sample_cases()
    else:
        tm.add_test_case(args.add)


if __name__ == '__main__':
    main()
