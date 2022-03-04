from pypinyin import lazy_pinyin, Style


def get_initials(str_data):
    """
       获取字符串的首字母
       :param str_data: 字符串
       :return: 返回首字母缩写(大写)
       """
    initials = ''.join(lazy_pinyin(str_data, style=Style.FIRST_LETTER))
    return initials.upper()[0]


print(get_initials("你好"))