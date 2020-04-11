from bs4 import BeautifulSoup as bs

def extract_task_screen_name(html, prob_type):
    soup = bs(html.text, 'html5lib')
    task_screen_name = ''
    for tr in soup.find('tbody').find_all('tr'):
        item = tr.find('td').find('a')
        p_type = item.contents[0].lower()
        link = item.get('href')
        if p_type == prob_type:
            # /contests/abc160/tasks/abc160_a という形式で取得できるので、
            # 最後の'abc160_a'の部分を取り出す
            task_screen_name = link.split('/')[-1]
            break
    return task_screen_name

def extract_csrf_token(html):
    soup = bs(html.text, 'lxml')
    csrf_token = soup.find(attrs={'name': 'csrf_token'}).get('value')
    return csrf_token
