BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
PURPLE = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'
END = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
INVISIBLE = '\033[08m'
REVERCE = '\033[07m'


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
    if color == 'white':
        return WHITE
    elif color == 'red' or color == 'r':
        return RED
    elif color == 'green' or color == 'g':
        return GREEN
    elif color == 'yellow':
        return YELLOW
    elif color == 'blue':
        return BLUE
    elif color == 'cyan':
        return CYAN
    else:
        return ''
