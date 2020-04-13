from typing import List

lang_ids = {
    'python': [3023, 4006],
    'pypy': [3510, 4047],
}

def get_lang_ids(lang_type: str) -> List[int]:
    if lang_type == 'p': return lang_ids['python']
    elif lang_type == 'pp': return lang_ids['pypy']
    else: return 0
