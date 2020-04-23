import subprocess
from argparse import ArgumentParser

if __name__ == '__main__':
    example = """
    ex: abc134の準備
        python {0} abc 134
    """.format(__file__)

    argparser = ArgumentParser(usage=example)
    argparser.add_argument('contest_type',
                           type=str,
                           help='コンテストの種類')
    argparser.add_argument('contest_id',
                           type=str,
                           help='コンテスト番号')

    args = argparser.parse_args()

    contest_type = args.contest_type
    contest_id = args.contest_id

    command_dir = ['python', 'makedir.py', contest_type, contest_id]
    subprocess.run(' '.join(command_dir), shell=True)

    command_test = ['python', 'testmake.py', contest_type, contest_id]
    subprocess.run(' '.join(command_test), shell=True)
