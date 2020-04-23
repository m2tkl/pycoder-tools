import os
import shutil
import config
from argparse import ArgumentParser
from libpycoder.pathmanager import PathManager

if __name__ == '__main__':
    example = """
    ex1: abc134のディレクトリを作成
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

    pm = PathManager(contest_type, contest_id)
    dir_name = pm.ATCODER_DIR
    file_names = ['A', 'B', 'C', 'D', 'E', 'F']
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    else:
        print('prog directory already exists')
    # プログラムファイル作成。テンプレートをコピー。
    for fn in file_names:
        if not os.path.exists(dir_name + fn + '.py'):
            if config.TEMPLATE_FILE:
                template = config.TEMPLATE_FILE
            else:
                template = './template/tempalte.py'
            shutil.copy(template, dir_name + fn + '.py')
    # テスト用のディレクトリを作成
    test_dir_name = pm.ATCODER_DIR + 'tests/'
    if not os.path.exists(test_dir_name):
        for fn in file_names:
            os.makedirs(test_dir_name + fn)
    else:
        print('test directory alread exists')
