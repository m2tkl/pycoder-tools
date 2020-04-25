UNDERLINE = '\033[4m'
INVISIBLE = '\033[08m'
REVERCE = '\033[07m'
END = '\033[0m'
BOLD = '\033[1m'

def switch(param):
    def value(dic):
        default = dic.get("default")
        return dic.get(param, default)
    return value

def paint(s: str, color='', bold=True) -> str:
    """stringを装飾する
    Args:
        s: 装飾対象の文字
        color: 色
        bold: 太字にするかどうか(デフォルトは太字)
    Returns:
        res: 装飾した文字
    """
    res = select_color(color) + s
    if bold:
        res = BOLD + res
    return res + END


def pprint(s: str, color='', bold=True, end=None) -> None:
    """文字を装飾してprintする
    Args:
        s: printする文字
        color: 色
        bold: 太字にするかどうか(デフォルトは太字)
        end: printのオプション
    """
    res = paint(s, color, bold)
    print(res, end=end)


def select_color(color: str) -> str:
    """指定された色のコードを返す
    Args:
        color: 色
    Returns:
        color-code: 色のコード
    """
    color_code = switch(color)({
            'black': '\033[30m',
            'red': '\033[31m',
            'green': '\033[32m',
            'yellow': '\033[33m',
            'blue': '\033[34m',
            'purple': '\033[35m',
            'cyan': '\033[36m',
            'white': '\033[37m',
            'default': ''})
    return color_code
