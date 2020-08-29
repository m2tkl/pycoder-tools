from typing import NamedTuple


class Contest(NamedTuple):
    type: str
    name: int


def split_contest_id(contest_id):
    """コンテスト名を分割する。
    :param contest_id: コンテスト名(ex: abc001, hogecon2020)
    :return Contest:
        abc001 => abc, 001
        hogecon2020 => others, 2020
    """
    if contest_id[:3] in ('abc', 'arc', 'agc'):
        return Contest(contest_id[:3], contest_id[3:])
    else:
        return Contest('others', contest_id)
