#!/usr/bin/env/ python
import fire
from . import judge as judgeCmd
from . import pycode


def login():
    pass


def contest(contest_id):
    """コンテストの準備をする
    :param contest_id: コンテストの名前(ex: abc001, hogecon2020)
    """
    pycode.set_contest(contest_id)


def addtest(contest_id, task):
    """テストケースを追加する
    :param contest_id: コンテストの名前(ex: abc001, hogecon2020)
    :param task: 追加対象の問題(a, b, c, ...)
    """
    pycode.add_test_case(contest_id, task)


def judge(contest_id, prob_type,
          verbose=False, error=None, debug=None,
          submit=None, force=False,):
    """テストケースの判定を行う
    :param contest_id: コンテストの名前(ex: abc001, hogecon2020)
    :param prob_type: 判定対象の問題(a, b, c, ...)
    :param verbose: 判定結果だけでなく入出力も表示する
    :param error: 誤差判定が必要なときに値を指定する
    :param submit: 提出オプション。すべてのテストケースに通過した場合提出する
    :param force: 提出オプション。テストケースに通過しなくても強制的に提出する
    :param debug: デバッグオプション。指定したテストケースのみを表示しつつ実行
    """
    judgeCmd.judge(contest_id, prob_type,
                   verbose=False, error=None, debug=None,
                   submit=None, force=False,)


def main():
    fire.Fire()


if __name__ == '__main__':
    main()
