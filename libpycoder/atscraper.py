from typing import Dict, List, Tuple
from bs4 import BeautifulSoup as bs

def extract_task_screen_name(html: str, prob_type: str) -> str:
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
    soup = bs(html, 'html5lib')
    csrf_token = soup.find(attrs={'name': 'csrf_token'}).get('value')
    return csrf_token

def extract_prob_links(html: str) -> Dict[str, str]:
    soup = bs(html, 'html5lib')
    prob_links = {'a': '', 'b': '', 'c': '', 'd': '', 'e': '', 'f': '',}
    for tr in soup.find('tbody').find_all('tr'):
        item = tr.find('td').find('a')
        p_type = item.contents[0].lower()
        link = item.get('href') # ex: /contests/abc160/tasks/abc160_a
        prob_links[p_type] = link
    return prob_links

def extract_sample_test_cases_from_prob_page(html: str) -> Dict[int, Tuple[str,str]]:
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
        # section内の先頭以外のpreは'間違いの例'などサンプルケースでないことがあるため、
        # 先頭のpreのみを取得する
        pre = sec.find('pre')
        # 問題文もsection内にあるが、問題文にはpreタグは存在しないため
        # preタグの有無でサンプルケースを取得することができる。
        if pre != None:
            io_samples.append(pre)

    sample_test_cases = {}
    for i in range(0, len(io_samples), 2):
        sample_test_cases[i//2] = (io_samples[i].get_text(), io_samples[i+1].get_text())
    return sample_test_cases
