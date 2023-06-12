from enum import Enum


class Color(Enum):
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    NORMAL = 5


def i(log_str: str):
    print_log_by_color(Color.NORMAL, log_str)


def v(log_str: str):
    print_log_by_color(Color.GREEN, log_str)


def w(log_str: str):
    print_log_by_color(Color.YELLOW, log_str)


def e(log_str: str):
    print_log_by_color(Color.RED, log_str)


def d(log_str: str):
    print_log_by_color(Color.BLUE, log_str)


def log_start(version_name: str, version_number: str):
    v(">>>>>>>Welcome Arno工具集 : 执行%s-版本:%s<<<<<<<" % (version_name, version_number))


def log_end(version_name: str, version_number: str):
    v(">>>>>>>执行%s完毕-版本:%s<<<<<<<" % (version_name, version_number))


def print_log_by_color(color_enum: Color, log_str: str):
    color_prefix = get_color_prefix(color_enum)
    color_suffix = "\033[0m"
    print(color_prefix + log_str + color_suffix)


# 色值对应
def get_color_prefix(color_enum: Color) -> str:
    if color_enum == Color.NORMAL:
        return "\033[38m"
    elif color_enum == Color.RED:
        return "\033[31m"
    elif color_enum == Color.GREEN:
        return "\033[32m"
    elif color_enum == Color.YELLOW:
        return "\033[33m"
    elif color_enum == Color.BLUE:
        return "\033[34m"
    else:
        return "\033[38m"
