#!/usr/bin/env/ python
import fire
from . import judge as judgeCmd
from . import pycode
from libpycoder.atsession import AtSession


class Commands:

    @staticmethod
    def login():
        AS = AtSession()
        AS.login()

    @staticmethod
    def logout():
        AS = AtSession()
        AS.logout()

    @staticmethod
    def chkin():
        AS = AtSession()
        AS.check_status()

    @staticmethod
    def contest(contest_id):
        """コンテストの準備をする
        :param contest_id: コンテストの名前(ex: abc001, hogecon2020)
        """
        pycode.set_contest(contest_id)

    @staticmethod
    def addtest(contest_id, task):
        """テストケースを追加する
        :param contest_id: コンテストの名前(ex: abc001, hogecon2020)
        :param task: 追加対象の問題(a, b, c, ...)
        """
        pycode.add_test_case(contest_id, task)

    def judge(self, contest_id, prob_type,
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
        # TODO: 00のみ何故か0として受け取ってしまうため変換している（01は01として受け取られている）
        if debug == 0:
            debug = '00'
        judgeCmd.judge(contest_id, prob_type,
                       verbose=verbose, error=error, debug=debug,
                       submit=submit, force=force)


def main():
    fire.Fire(Commands)
    # fire.Fire(AtSession)


if __name__ == '__main__':
    main()
