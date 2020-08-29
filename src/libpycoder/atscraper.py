from typing import Dict, Tuple
from bs4 import BeautifulSoup as bs
from collections import namedtuple


def extract_task_screen_name(html: str, prob_type: str) -> str:
    """コンテスト問題一覧ページから、prob_typeで指定された問題の名前を取得
    @param html コンテストの問題一覧ページ
    @param prob_type 問題のタイプ(a,b,c,...)
    @return task_screen_name 問題の名前
        ex: abc160_a
        !! 必ずしもコンテスト番号、問題のタイプと、
        取得するtask_screen_nameは一致しない。
        例えば、abc123のa問題のtask_screen_nameがarc012_bということがある。
    """
    prob_links = extract_prob_links(html)
    task_screen_name = ''
    for p_type, link in prob_links.items():
        if p_type == prob_type:
            # /contests/abc160/tasks/abc160_a という形式で取得できるので、
            # 最後の'abc160_a'の部分を取り出す
            task_screen_name = link.split('/')[-1]
            break
    return task_screen_name


def extract_csrf_token(html: str) -> str:
    """htmlからcsrfトークンを取得する.
    @param html csrfトークンを取得したいページ
    @return csrf_token
    """
    soup = bs(html, 'html5lib')
    csrf_token = soup.find(attrs={'name': 'csrf_token'}).get('value')
    return csrf_token


def extract_prob_links(html: str) -> Dict[str, str]:
    """問題一覧ページから各問題へのパスを取得する.
    @param html 問題一覧ページ
    @return prob_links 各問題のパス
    """
    soup = bs(html, 'html5lib')
    prob_links = {}
    for tr in soup.find('tbody').find_all('tr'):
        item = tr.find('td').find('a')
        p_type = item.contents[0].lower()
        link = item.get('href')  # ex: /contests/abc160/tasks/abc160_a
        prob_links[p_type] = link
    return prob_links


def extract_sample_test_cases_from_prob_page(
        html: str) -> Dict[int, Tuple[str, str]]:
    """問題ページからサンプルテストケースを抽出する.
    @param html 問題ページ
    @return 問題ページのサンプルテストケース.
        {0: (入力例1, 出力例1), 1: (入力例2, 出力例2), ...}といった形式の辞書で返す.
    """
    soup = bs(html, 'html5lib')
    # 英語ページを除外（日本語ページのサンプルケースと重複して取得してしまうのを防ぐため）
    while soup.find('span', class_='lang-en'):
        soup.find('span', class_='lang-en').extract()
    # 入出力の形式欄を除外
    while soup.find('div', class_='io-style'):
        soup.find('div', class_='io-style').extract()

    io_samples = []
    for sec in soup.find_all('section'):
        if sec.find('h3').get_text() == '問題文':
            continue
        # section内の先頭以外のpreは'間違いの例'などサンプルケースでないことがあるため、
        # 先頭のpreのみを取得する
        pre = sec.find('pre')
        if pre is None:
            continue
        io_samples.append(pre.get_text())

    TestCase = namedtuple('TestCase', ['input', 'output'])
    sample_test_cases = {}
    for i in range(0, len(io_samples), 2):
        try:
            sample_test_cases[i//2] = TestCase(io_samples[i],
                                               io_samples[i+1])
        except IndexError:
            sample_test_cases[i//2] = None
    return sample_test_cases
